from dataclasses import dataclass
from typing import Union

@dataclass
class ArincWord:
    """
    Container for an ARINC 429 word.

    """
    label: int = 0
    byte1: int = 0
    byte2: int = 0
    byte3: int = 0
    byte4: int = 0
    encoding: str = ""
    msb: int  = 0
    lsb: int  = 0
    sdi: int = 0
    ssm: int = 0
    value: Union[int, float] = 0
    offset: Union[int, float] = 0
    scale:  float = 1
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
        """Returns a string visualization of the ARINC word bits in markdown table format

        Like this :
        |32|31|30|29|28|27|26|25|24|23|22|21|20|19|18|17|16|15|14|13|12|11|10|9 |8 |7 |6 |5 |4 |3 |2 |1 |
        |--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
        |0 |1 |1 |0 |0 |0 |0 |0 |0 |0 |1 |1 |1 |1 |1 |1 |1 |0 |0 |0 |0 |0 |0 |0 |1 |1 |0 |1 |1 |0 |1 |1 |

        This is really useful for debugging purposes or to visualize the bits of an ARINC word

        """
        bits = []
        for byte in [self.byte4, self.byte3, self.byte2, self.byte1]:
            bits.extend([str((byte >> i) & 1) for i in range(7,-1,-1)])
        
        header = "|" + "|".join(f"{i:^2d}" for i in range(32,0,-1)) + "|"
        separator = "|" + "|".join("--" for _ in range(32)) + "|"
        bits_str = "|" + "|".join(f"{b:^2}" for b in bits) + "|"
        return f"{header}\n{separator}\n{bits_str}"


def reverse_label(label: int) -> int:
    """
    Reverses the bits of an 8-bit unsigned integer using bitwise operations.
    """
    if not 0 <= label <= 255:
        raise ValueError("Input must be an 8-bit unsigned integer (0 <= n <= 255).")

    label = ((label & 0b11110000) >> 4) | ((label & 0b00001111) << 4)
    label = ((label & 0b11001100) >> 2) | ((label & 0b00110011) << 2)
    label = ((label & 0b10101010) >> 1) | ((label & 0b01010101) << 1)

    return label
