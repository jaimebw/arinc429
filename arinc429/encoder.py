from typing import Union



class Encoder:
    def __init__(self)->None:
        # General stuff
        self.data:Union[int,float] = 0
        self.label:int = 0
        self.sdi:int = 0
        self.ssm:int = 0
        self.value:Union[int, float] = 0
        self.encoding:str = ""
        self.msb:int = 29
        self.lsb:int = 11
        # BRN encoding
        self.offset:Union[int,float] = 0
        self.scale:Union[int, float] = 1
        # BCD encoding
        self.word:int = 0
        self.b_arr: bytes = b"0"

        #
    def __repr__(self)->str:
        return f"""Arinc429Encoder(label={self.label}, 
                sdi={self.sdi}, ssm={self.ssm}, value={self.value}, 
                encoding={self.encoding}, data={self.data}
                word ={hex(self.word)})"""

    def encode(self, value:Union[int, float] = 0, 
               msb:int = 29, 
               lsb:int = 11,
               label:int=0,
               sdi:int= 0,
               ssm:int= 0,
               scale:float = 1,
               offset:float = 0,
               encoding:str="")->None:
        self.value = value
        self.label = label
        self.sdi = sdi
        self.ssm = ssm
        self.encoding = encoding
        self.msb = msb
        self.lsb = lsb
        self.offset = offset
        self.scale = scale
        if self.encoding == "BNR":
            self._encode_bnr()
        elif self.encoding == "BCD":
            raise NotImplementedError("BCD encoding not implemnted yet :(")
            self._encode_bcd()
        elif self.encoding == "DSC":
            raise NotImplementedError("DSC encoding not implemnted yet :(")
            self._encode_dsc()
        else:
            raise ValueError(f"Encoding {self.encoding} not supported")

        self._check_sdi()
        self._check_ssm()
        self._check_msb()
        self._check_lsb()

    def _check_sdi(self):
        if not 0<=self.sdi<=0x03:
            raise ValueError("The SDI cannot be negative or bigger than 0x03")
    def _check_ssm(self):
        if not 0<=self.ssm<=0x03:
            raise ValueError("The SSM cannot be negative or bigger than 0x03")
    def _check_msb(self):
        if not 11<=self.msb<=29:
            raise ValueError("The most significant bit cannot be bigger than 29 or smaller than 11")
    def _check_lsb(self):
        if not 9<=self.lsb<=29:
            raise ValueError("The least significant bit cannot be bigger than 29 or smaller than 9")



    def _encode_bnr(self):
        """
        Encode following the BNR schema

        data = (value - offset) / offset
        """
        self.data = (self.value -self.offset) / self.scale

        # Byte1 - label
        byte1 = self._reverse_label(self.label)
        # Byte2 - SDI + some word stuff
        if (self.sdi == 0) and ( (self.lsb >9) &(self.lsb<11)):
            # lsb = 10
            mov= 11 - self.lsb
        else:
            mov= 2

        byte2 = self.sdi
        byte2 |= (int(self.data)) << mov
        byte2 &= 0xFF
        # Byte 3: Data
        byte3 = 0
        byte3 |= (int(self.data) >> (mov+4))
        byte3 &= 0xFF

        # Byte 4- Data + SSM + Parity
        byte4  = 0
        byte4 |= (int(self.data) >> (mov +8)) & 0x3F
        byte4 |= self.ssm  << 5

        parity= self._get_parity(bytes([byte1,byte2,byte3,byte4]))

        if parity: # If not, the parity is already set to zero
            byte4 |= 0x80

        self.b_arr = bytes([byte4,byte3,byte2,byte1])

        self.word = int.from_bytes(self.b_arr, byteorder='little', signed=False)

    def _get_mask(self,n: int) -> int:
        """
        Returns an 8-bit mask with the first n bits set to 0 and the rest set to 1.

        Parameters:
            n (int): The number of leading bits to mask (0 <= n <= 8).

        Returns:
            int: The mask as an 8-bit integer.
        """
        if n < 0 or n > 8:
            raise ValueError("n must be between 0 and 8.")
    
        return 0xFF >> n
        
    def _encode_bcd(self):

        pass
    def _encode_dsc(self):

        pass

    def _get_parity(self, b_data: bytes) -> bool:
        """
        Computes the odd parity for the entire 32-bit ARINC429 word.
        Returns True if parity bit should be 1, False if it should be 0
        to maintain odd parity.
        """
        # Count all 1 bits in the entire word (excluding the parity bit)
        num_ones = 0
        for byte in b_data:
            # For the last byte, mask out the parity bit (MSB)
            if byte == b_data[-1]:
                byte &= 0x7F
            num_ones += bin(byte).count('1')
        
        return num_ones % 2 == 0

    def _reverse_label(self,label:int)->int:
        """
        Reverses the bits of an 8-bit unsigned integer using bitwise operations.
        """
        if not 0 <= label <= 255:
            raise ValueError("Input must be an 8-bit unsigned integer (0 <= n <= 255).")

        label = ((label & 0b11110000) >> 4) | ((label & 0b00001111) << 4)
        label = ((label & 0b11001100) >> 2) | ((label & 0b00110011) << 2)
        label = ((label & 0b10101010) >> 1) | ((label & 0b01010101) << 1)
        self.rlabel = label


        return label


    def get_data(self):
        return self.data

