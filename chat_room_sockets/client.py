# Author: gabri
# File: client
# Date: 01/10/2019
# Made with PyCharm

# Standard Library
import select
import queue
import threading
import sys
import socket

# Third party modules

# Local application imports
from msg_trader import MessagesExchanger


class ClientToServerConnection:
    final_response_codes = [105]

    def __init__(self, sock: socket.socket, timeout):
        self.socket = sock
        self.msg_trader = MessagesExchanger(sock)
        self.online = threading.Event()
        self.sent_codes = queue.Queue()
        self.msgs_to_send = queue.Queue()
        self.msgs_handler = threading.Thread(
            target=self.communication_handler, args=(timeout,))
        self.connected_to_server = True
        self.new_msg = False

    def chat_interface(self, connection_timeout):
        print("\nChat\n")
        self.send_nickname_check()

        if self.online.wait(timeout=connection_timeout):
            while self.online.is_set():
                print("\nOptions")
                print("1- Users list")
                print("2- Public msg")
                print("3- Private msg")
                print("4- Disconnect\n")
                option = int(input())

                if option == 1:
                    self.request_users_list()
                elif option == 2:
                    self.send_public_msg()
                elif option == 3:
                    self.send_private_msg()
                elif option == 4:
                    self.request_disconnection()
                else:
                    print("\nWrong option\n")
        else:
            print("\nToo much time waiting for server response.\n")

    def send_nickname_check(self):
        nickname = input("Enter your nickname: ")
        data = bytes(f"{chr(100)}{nickname}", "utf-8")
        self.msgs_to_send.put((100, data))

    def request_users_list(self):
        self.msgs_to_send.put((104, bytes(chr(104), "utf-8")))

    def send_public_msg(self):
        msg = input("\nMensagem: ")
        data = bytes(f"{chr(101)}{msg}", "utf-8")
        self.msgs_to_send.put((101, data))

    def send_private_msg(self):
        nickname = input("\nDestination nickname: ")
        msg = input("Message: ")
        data = bytes(f"{chr(102)}{nickname}:{msg}", "utf-8")
        self.msgs_to_send.put((102, data))

    def request_disconnection(self):
        self.msgs_to_send.put((103, bytes(chr(103), "utf-8")))

    def communication_handler(self, timeout):
        while self.connected_to_server:
            read_socket, _, _ = select.select([self.socket], [], [], timeout)
            if read_socket:
                try:
                    self.read_msg()
                except OSError:
                    raise
                self.check_codes()
            self.send_msgs()
        self.close_connection(0)

    def read_msg(self):
        msg = self.msg_trader.recv_msg()

        if msg is not None:
            self.recv_code, self.msg_content = msg[0], msg[1:]
            self.new_msg = True

    def send_msgs(self):
        while True:
            try:
                code, data = self.msgs_to_send.get_nowait()
            except queue.Empty:
                return

            if code not in self.final_response_codes:
                self.sent_codes.put(code)
            self.msg_trader.send_msg(data)

    def check_codes(self):
        if self.new_msg:
            self.new_msg = False

            if self.recv_code == 109:  # Public or private msg
                self.show_msg()

            elif self.recv_code == 110:  # Keep alive
                self.respond_user_connection_check()

            else:  # Client requested action
                self.sent_code = self.sent_codes.get()

                if self.sent_code == 100:  # Login
                    if self.recv_code == 105:
                        print("\nUser connected successfully!\n")
                        self.online.set()
                    elif self.recv_code == 108:
                        print("\nInvalid nickname\n")
                        self.disconnect()
                    else:
                        print("Unknown response from server")

                elif self.sent_code == 101:  # Public msg
                    if self.recv_code == 105:
                        pass
                    else:
                        print("Unknown response from server")

                elif self.sent_code == 102:  # Private msg
                    if self.recv_code == 105:
                        pass
                    elif self.recv_code == 106:
                        print("\nNickname not connected\n")
                    else:
                        print("Unknown response from server")

                elif self.sent_code == 103:  # Disconection
                    if self.recv_code == 105:
                        self.disconnect()
                    else:
                        print("Unknown response from server")

                elif self.sent_code == 104:  # Users list
                    if self.recv_code == 107:
                        self.show_users_list()
                    else:
                        print("Unknown response from server")
                else:
                    print("Error when trying to execute requested command")

    def show_msg(self):
        self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))
        print(self.msg_content.decode("utf-8"))

    def respond_user_connection_check(self):
        self.msgs_to_send.put((105, bytes(chr(105), "utf-8")))

    def show_users_list(self):
        print("\nOnline users list:")
        print("\n".join(self.msg_content.decode("utf-8").split("|")))

    def disconnect(self):
        self.online.clear()
        self.connected_to_server = False

    def close_connection(self, code):
        self.socket.close()
        print("\nThank you for joining the chat!\n")
        sys.exit(0)



def main():
    ip = socket.gethostname()
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    client = ClientToServerConnection(sock, 0.5)
    client.msgs_handler.start()
    client.chat_interface(5.0)


if __name__ == "__main__":
    main()
