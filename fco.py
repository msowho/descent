from binary import Binary
from typing import IO


class FCO(Binary):
    def __init__(self, io: IO) -> None:
        super().__init__(io, "ascii", "big")

        self.groups = []

    def read_fco(self, offset: int = 0):
        self.move_to_position(offset)

        # i will use 00 00 00 04 00 00 00 00 as magic header
        assert self.read_bytes(8) == b"\x00\x00\x00\x04\x00\x00\x00\x00"

        self.groups = []

        group_count = self.read_integer()

        for i in range(group_count):
            group_name = self.read_string()

            message_count = self.read_integer()
            messages = []

            for j in range(message_count):
                message_name = self.read_string()

                symbol_count = self.read_integer()
                message_symbols = []

                for l in range(symbol_count):
                    symbol_code = self.read_integer()
                    message_symbols.append(symbol_code)
                
                # 00 00 00 04 00 00 00 00 means end of message
                assert self.read_bytes(8) == b"\x00\x00\x00\x04\x00\x00\x00\x00"

                unknown_1 = self.read_bytes(4)
                self.move_to_position(4, from_start=False, from_current=True)
                
                # FF FF FF FF 00 00 00 00 means termination (???)
                assert self.read_bytes(8) == b"\xFF\xFF\xFF\xFF\x00\x00\x00\x00"

                # Skipping the unknown bytes (probably "second" variation)
                # TODO: Needed to make it work with all FCO files
                while self.read_bytes(4) == unknown_1:
                    self.move_to_position(12, from_start=False, from_current=True)

                message = {
                    "name": message_name,
                    "symbols": message_symbols
                }

                messages.append(message)
            
            group = {
                "name": group_name,
                "messages": messages
            }

            self.groups.append(group)
    
    @staticmethod
    def create_empty():
        io = IO()
        return FCO(io)
