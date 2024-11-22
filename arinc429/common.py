from dataclasses import dataclass
from typing import Union

@dataclass
class ArincWord:
    label: int = 0
    byte1: int = 0
    byte2: int = 0
    byte3: int = 0
    byte4: int = 0
    encoding: str = ""
    msb: Union[int, None] = None
    lsb: Union[int, None] = None
    sdi: int = 0
    ssm: int = 0
    value: Union[int, float] = 0
    offset: Union[int, float, None] = None
    scale: Union[int, float, None] = None
    data: Union[int, float] = 0

    def __repr__(self):
                return f"ArincWord(0x{self.byte1:02x},0x{self.byte2:02x},0x{self.byte3:02x},0x{self.byte4:02x})"
    @property
    def word(self):
        return int.from_bytes(bytes([self.byte1,self.byte2,self.byte3,self.byte4]),byteorder="little",signed=False)

    def get_bytes(self)->bytes:
        return bytes([self.byte4,self.byte3,self.byte2,self.byte1])

    @property
    def parity(self):
        return self.byte4 & 0x80

    def visualize(self)->str:
        """Returns a string visualization of the ARINC word bits in markdown table format"""
        bits = []
        for byte in [self.byte4, self.byte3, self.byte2, self.byte1]:
            bits.extend([str((byte >> i) & 1) for i in range(7,-1,-1)])
        
        header = "|" + "|".join(f"{i:^2d}" for i in range(32,0,-1)) + "|"
        separator = "|" + "|".join("--" for _ in range(32)) + "|"
        bits_str = "|" + "|".join(f"{b:^2}" for b in bits) + "|"
        return f"{header}\n{separator}\n{bits_str}"
