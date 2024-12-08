from .common import ArincWord,reverse_label
import struct
from typing import List,Union


class Decoder:
    def __init__(self):
        self.dword:ArincWord = ArincWord()

    def decode(self, 
               word: Union[int, List[int],bytes],
               encoding: str,
               msb: int = 29,
               lsb: int = 11,
               scale: float = 1,
               offset: float = 0,
               sdi: int = 0,
               ssm: int = 0
               )->ArincWord:
        """
        Decode main function.


        Parameters
        ----------
        word : Union[int, List[int],bytes]
            The ARINC word to decode. It can be an integer, a list of integers or a bytes object.
        encoding : str
        msb : int, Most significant bit
        lsb : int, Least significant bit
        scale : float
        offset : float
        sdi : int
        ssm : int
        """
        if isinstance(word, int):
            word = struct.pack("<I",word)
        elif isinstance(word, list):
            word = bytes(word)
        elif isinstance(word, bytes):
            pass


        self.dword.encoding = encoding
        self.dword.byte1 = word[0]
        self.dword.byte2 = word[1]
        self.dword.byte3 = word[2]
        self.dword.byte4 = word[3] # Label
        self.dword.msb = msb
        self.dword.lsb = lsb
        self.dword.scale = scale
        self.dword.offset = offset
        self.dword.sdi = sdi
        self.dword.ssm = ssm

        self._decode_label()
        self._decode_sdi_ssm()

        if encoding == "BCD":
            return self._decode_bcd()
        elif encoding == "BNR":
            return self._decode_bnr()
        elif encoding == "DSC":
            return self._decode_dsc()
        else:
            raise ValueError("Unknown encoding")

    def _decode_label(self):
        self.dword.label = reverse_label(self.dword.byte4)

    def _decode_bcd(self)->ArincWord:
        pass
        return self.dword

    def _decode_sdi_ssm(self):

        if self.dword.lsb<11:
            self.dword.sdi = 0
        else:
            self.dword.sdi = self.dword.byte3 & 0x03

        if self.dword.msb>29:
            self.dword.ssm = 0
        else:
            self.dword.ssm = (self.dword.byte1 & 0x60) >> 5




    def _decode_bnr(self)->ArincWord:
        """
         I need to get from the bytes, the ssm, the sdi, the parity and the value

        edata = (value - offset)/scale

        TODO: Add the MSB and LSB
        """

        self.dword.data = ((self.dword.byte1 & 0x1F)<<14) | ((self.dword.byte2)<<6) | ((self.dword.byte3 & 0xFC)>>2)
        self.dword.value = float(self.dword.data) * self.dword.scale + self.dword.offset
        return self.dword

    def _decode_dsc(self)->ArincWord:
        pass
        return self.dword
