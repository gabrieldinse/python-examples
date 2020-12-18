# Author: gabri
# File: server
# Date: 01/10/2019
# Made with PyCharm

# Standard Library
import socket
import select
import threading
import queue
import time
import sys
import re

# Third party modules


# Local application imports
from messages_exchanger import MessagesExchanger


class ServerToClientConnection:
    final_response_codes = [105, 106, 107, 108]

    def __init__(self, sock: socket.socket, clients,
                 clients_list_lock, nickname_regex):
        self.socket = sock
        self.clients = clients
        self.clients_list_lock = clients_list_lock
        self.nickname_match = re.compile(nickname_regex)
        self.messages_exchanger = MessagesExchanger(sock)
        self.nickname = "##NOT_CONNECTED##"
        self.msgs_to_send = queue.Queue()
        self.sent_codes = queue.Queue()
        self.keepalive_timer = time.time()
        self.msgs_handler = threading.Thread(
            target=self.communication_handler, args=(0.5,))
        self.connected_to_server = True
        self.online = False
        self.new_msg = False
        self.waiting_connection_confirmation = False

    def communication_handler(self, timeout):
        while self.connected_to_server:
            read_socket, _, _ = select.select([self.socket], [], [], timeout)
            if read_socket:
                try:
                    self.read_message()
                except OSError as e:
                    print(f"Error reading socket from {self.nickname} "
                          f"{self.socket.getsockname()}")
                    break
                self.check_codes()
            self.send_messages()
            self.check_user_connection()
        self.close_connection()

    def send_messages(self):
        while True:
            try:
                code, data = self.msgs_to_send.get_nowait()
            except queue.Empty:
                return

            if code not in self.final_response_codes:
                self.sent_codes.put(code)
            self.messages_exchanger.send_message(data)
            print(f"Code {code} sent to {self.nickname} "
                  f"{self.socket.getsockname()}")

    def read_message(self):
        msg = self.messages_exchanger.receive_message()

        if msg is not None:
            self.recv_code, self.msg_content = msg[0], msg[1:]
            print(f"Code {self.recv_code} received from {self.nickname} "
                  f"{self.socket.getsockname()}")
            self.new_msg = True

    def check_codes(self):
        if self.new_msg:
            self.new_msg = False

            if self.recv_code == 100:  # Login request
                self.check_nickname()

            elif self.recv_code == 101:  # Public msg
                self.post_public_msg()

            elif self.recv_code == 102:  # Private msg
                self.post_private_msg()

            elif self.recv_code == 103:  # Disconnection
                self.disconnect()

            elif self.recv_code == 104:  # Users list
                self.send_users_list()

            else:  # Client requested action
                self.sent_code = self.sent_codes.get()

                if self.sent_code == 109:  # Public or private msg
                    if self.recv_code == 105:
                        pass
                    else:
                        print(f"Unknown response from {self.nickname} "
                              f"{self.socket.getsockname()}")

                elif self.sent_code == 110:  # Keepalive
                    if self.recv_code == 105:
                        self.keepalive()
                    else:
                        print(f"Unknown response from {self.nickname} "
                              f"{self.socket.getsockname()}")

    def check_nickname(self):
        nickname = self.msg_content.decode("utf-8")
        if self.nickname_match.match(nickname):  # Nickname matchs regex
            with self.clients_list_lock:
                for client in self.clients:
                    if client.online and client.nickname == nickname:
                        self.msgs_to_send.put(
                            (108, bytes(chr(108), "utf-8")))
                        return
                self.nickname = nickname
                self.online = True
                for client in self.clients:
                    if client.online and client is not self:
                        data = bytes(f"{chr(109)}(Public) {self.nickname} "
                                     "connected", "utf-8")
                        client.msgs_to_send.put((109, data))
            self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))
            print(f"Client {self.nickname} {self.socket.getsockname()} "
                  "connected")
        else:  # Nickname doesn't match
            self.msgs_to_send.put((108, bytes(chr(108), "utf-8")))

    def post_public_msg(self):
        self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))
        with self.clients_list_lock:
            for client in self.clients:
                if client.online and client is not self:
                    data = bytes(f"{chr(109)}(Public) {self.nickname}:"
                                 f" {self.msg_content.decode('utf-8')}",
                                 "utf-8")
                    client.msgs_to_send.put((109, data))

    def post_private_msg(self):
        nickname, msg = self.msg_content.decode("utf-8").split(":")
        with self.clients_list_lock:
            for client in self.clients:
                if client.online and client.nickname == nickname:
                    self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))
                    data = bytes(f"{chr(109)}(Private) {self.nickname}:"
                                 f" {msg}",
                                 "utf-8")
                    client.msgs_to_send.put((109, data))
                    return
            self.msgs_to_send.put((106, bytes(chr(106), "utf-8")))

    def disconnect(self):
        self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))
        self.connected_to_server = False

    def send_users_list(self):
        with self.clients_list_lock:
            nicknames_list = []
            for client in self.clients:
                if client is not self:
                    nicknames_list.append(client.nickname)
            data = bytes(f"{chr(107)}" + "|".join(nicknames_list), "utf-8")
            self.msgs_to_send.put((107, data))

    def keepalive(self):
        self.keepalive_timer = time.time()
        self.waiting_connection_confirmation = False

    def check_user_connection(self):
        if self.waiting_connection_confirmation:
            if time.time() - self.keepalive_timer >= 40.0:
                self.disconnect()
        elif time.time() - self.keepalive_timer >= 30.0:
            self.send_user_connection_check()
            self.waiting_connection_confirmation = True

    def send_user_connection_check(self):
        with self.clients_list_lock:
            data = bytes(f"{chr(110)}", "utf-8")
            self.msgs_to_send.put((110, data))

    def close_connection(self):
        with self.clients_list_lock:
            for client in self.clients:
                if client is self:
                    self.clients.remove(self)
                    print(f"Number of connected clients: {len(self.clients)}")
                    break
        print(f"Client {self.nickname} "
              f"{self.socket.getsockname()} disconnected")
        self.socket.close()


class Server:
    def __init__(self, sock, nickname_regex):
        self.socket = sock
        self.clients = []
        self.nickname_regex = nickname_regex
        self.clients_list_lock = threading.Lock()
        self.online = False

    def connection_interface(self):
        self.socket.listen(10)  # Queue of connection requests
        self.online = True
        print("\nServer started\n")
        while self.online:
            client_socket, address = self.socket.accept()
            client = ServerToClientConnection(
                client_socket, self.clients, self.clients_list_lock,
                self.nickname_regex)
            client.msgs_handler.start()
            with self.clients_list_lock:
                self.clients.append(client)


def main():
    ip = socket.gethostname()
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reuse address when reconnect
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server = Server(server_socket, "[A-Za-z0-9]")  #"^[^0-9][^@#]{1, 32}$")
    server.connection_interface()


if __name__ == "__main__":
    main()
