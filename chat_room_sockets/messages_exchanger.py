# Author: gabri
# File: messages_passing_socket
# Date: 05/10/2019
# Made with PyCharm

# Standard Library
import socket
import struct
from enum import Enum

# Third party modules

# Local application imports


class HeaderSize(Enum):
    UINT8 = 1
    UINT16 = 2
    UINT32 = 3
    UINT64 = 4


class MessagesExchanger:
    def __init__(self, sock, header_size : HeaderSize=HeaderSize.UINT32):
        self.socket = sock
        self.packer = struct.Struct(self._get_format(header_size))

    @staticmethod
    def _get_format(header_size : HeaderSize):
        if header_size == HeaderSize.UINT8:
            return "B"
        elif header_size == HeaderSize.UINT16:
            return "H"
        if header_size == HeaderSize.UINT32:
            return "I"
        if header_size == HeaderSize.UINT64:
            return "Q"

    def _recv_n_bytes(self, number_of_bytes, max_size=4096):
        data = bytearray()
        while (remaining := number_of_bytes - len(data)) > 0:
            packet_size = remaining if remaining < max_size else max_size
            packet = self.socket.recv(packet_size)
            if not packet:
                return None
            data.extend(packet)
        return data

    def receive_message(self):
        # Get message length
        header = self._recv_n_bytes(struct.calcsize(self.packer.format))
        if not header:
            return None

        message_len = self.packer.unpack(header)[0]
        return self._recv_n_bytes(message_len)

    def send_message(self, message):
        self.socket.sendall(self.packer.pack(len(message)) + message)


def main():
    pass


if __name__ == "__main__":
    main()
