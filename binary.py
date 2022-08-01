from typing import IO, Literal


class Binary:
    def __init__(self,
                io: IO,
                char_encoding: str,
                byteorder: Literal["little", "big"] = "little") -> None:
        self._io = io
        self.byteorder = byteorder
        self.char_encoding = char_encoding
    
    @property
    def avaliable_bytes(self) -> int:
        return self._io.tell()
    
    def move_to_position(self,
                         offset: int,
                         from_start: bool = True,
                         from_current: bool = False,
                         from_end: bool = False) -> int:
        if from_start: return self._io.seek(offset, 0)
        elif from_current: return self._io.seek(offset, 1)
        elif from_end: return self._io.seek(offset, 2)
        else: return 0

    def read_bytes(self, size: int) -> bytes:
        if not self._io.readable() or size > self.avaliable_bytes: return b'\x00' * size
        return self._io.read(size)
    
    def write_bytes(self, source: bytes) -> int:
        if not self._io.writable(): return 0
        return self._io.write(source)
    
    def read_integer(self, size: int = 4) -> int:
        serialized_integer = self.read_bytes(size)
        return int.from_bytes(serialized_integer, self.byteorder)
    
    def write_integer(self, integer: int = 0, size: int = 4) -> int:
        serialized_integer = integer.to_bytes(size, self.byteorder)
        return self.write_bytes(serialized_integer)
    
    def read_char(self, size: int = 1) -> str:
        serialized_char = self.read_bytes(size)
        return serialized_char.replace(b"\x00", b"").decode(self.char_encoding)
    
    def write_char(self, source: str, size: int = 1) -> int:
        serialized_char = source.rjust("\0").encode(self.char_encoding)
        return self.write_bytes(serialized_char)
    
    def read_string(self) -> str:
        length = self.read_integer()
        char = self.read_char(length)

        while self.avaliable_bytes % 4 == 0:
            if length == 0:
                break
            
            assert self.read_char() == "@"
        
        return char
    
    def write_string(self, string: str) -> None:
        length = len(string)

        self.write_integer(length)
        self.write_char(string, length)

        while length % 4 == 0:
            self.write_char("@")
            length += 1
