# Author: gabri
# File: messages_passing_socket
# Date: 05/10/2019
# Made with PyCharm

# Standard Library
import socket
import struct

# Third party modules

# Local application imports


class MessagesExchanger:
    def __init__(self, sock):
        self.socket = sock
    
    def _recv_n_bytes(self, number_of_bytes):
        data = b""
        while len(data) < number_of_bytes:
            packet = self.socket.recv(number_of_bytes - len(data))
            if not packet:
                return None
            data += packet
        return data

    def recv_message(self):
        # Get message length
        header = self._recv_n_bytes(4)  # int
        if not header:
            return None

        message_len = struct.unpack(">I", header)[0]
        return self._recv_n_bytes(message_len)

    def send_message(self, message):
        self.socket.sendall(struct.pack(">I", len(message)) + message)


def main():
    pass


if __name__ == "__main__":
    main()
