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
    def __init__(self, sock, header_format='I'):
        self.socket = sock
        self.packer = struct.Struct(header_format)

    def _recv_n_bytes(self, number_of_bytes, max_size=4096):
        data = bytearray()
        while (remaining := number_of_bytes - len(data)) > 0:
            packet_size = remaining if remaining < max_size else max_size
            packet = self.socket.recv(packet_size)
            if not packet:
                return None
            data.extend(packet)
        return data

    def recv_message(self):
        # Get message length
        header = self._recv_n_bytes(4)  # int
        if not header:
            return None

        message_len = self.packer.unpack(header)[0]
        return self._recv_n_bytes(message_len)

    def send_message(self, message):
        self.socket.sendall(self.packer.pack(">I", len(message)) + message)


def main():
    pass


if __name__ == "__main__":
    main()
