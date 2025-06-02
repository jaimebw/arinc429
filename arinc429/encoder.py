from typing import Union, List
from .common import ArincWord, reverse_label




class Encoder:
    def __init__(self) -> None:
        """Initialize an ARINC429 encoder with default values.

        Attributes:
            data (Union[int,float]): The encoded data value after processing
            label (int): 8-bit ARINC429 label (0-255)
            sdi (int): Source/Destination Identifier (0-3)
            ssm (int): Sign/Status Matrix (0-3)
            value (Union[int,float]): Raw input value before encoding
            encoding (str): Encoding type ("BNR", "BCD", or "DSC")
            msb (int): Most Significant Bit position (11-29)
            lsb (int): Least Significant Bit position (9-29)
            offset (Union[int,float]): BNR encoding offset value
            scale (Union[int,float]): BNR encoding scale factor
            word (int): Final 32-bit ARINC429 word
            b_arr (bytes): Byte array representation of the ARINC word
        """
        # Byte list in int
        self.a429vals: List[ArincWord] = []

    def __repr__(self) -> str:
        return '\n'.join([str(word) for word in self.a429vals])
    def __getitem__(self, index: int):
        return self.a429vals[index]
    def encode(
        self,
        value: Union[int, float] = 0,
        msb: int = 29,
        lsb: int = 11,
        label: int = 0,
        sdi: int = 0,
        ssm: int = 0,
        scale: float = 1,
        offset: float = 0,
        encoding: str = "",
    ) -> None:
        """Encode a value into an ARINC429 word.

        Args:
            value (Union[int, float], optional): The value to encode. Defaults to 0.
            msb (int, optional): Most Significant Bit position (11-29). Defaults to 29.
            lsb (int, optional): Least Significant Bit position (9-29). Defaults to 11.
            label (int, optional): 8-bit ARINC429 label (0-255). Defaults to 0.
            sdi (int, optional): Source/Destination Identifier (0-3). Defaults to 0.
            ssm (int, optional): Sign/Status Matrix (0-3). Defaults to 0.
            scale (float, optional): Scale factor for BNR encoding. Defaults to 1.
            offset (float, optional): Offset value for BNR encoding. Defaults to 0.
            encoding (str, optional): Encoding type ("BNR", "BCD", "DSC" or "BNU"). Defaults to "".

        Raises:
            ValueError: If the encoding type is not supported or if parameters are invalid.
        """
        self.reset()
        self._check_sdi(sdi)
        self._check_ssm(ssm)
        self._check_msb(msb)
        self._check_lsb(lsb)

        if encoding == "BNR":
            self._encode_bnr(encoding,label,msb,lsb,sdi,ssm,scale,offset,value)
        elif encoding == "BCD":
            self._encode_bcd(encoding,label,sdi,ssm,int(value))
        elif encoding == "DSC" or encoding == "BNU":
            self._encode_dsc(encoding,label,msb,lsb,sdi,ssm,int(value))
        else:
            raise ValueError(f"Encoding {encoding} not supported")


    def _check_sdi(self,sdi:int):
        """
        Check if the SDI has a valid value
        """
        if not 0 <= sdi <= 0x03:
            raise ValueError("The SDI cannot be negative or bigger than 0x03")
        # if self.lsb < 11 and self.sdi != 0:
        #     raise ValueError("SDI must be 0 if LSB is smaller than 11")

    def _check_ssm(self,ssm):
        """
        Check if the SSM has a valid value
        """
        if not 0 <= ssm <= 0x03:
            raise ValueError("The SSM cannot be negative or bigger than 0x03")

    def _check_msb(self,msb:int)->None:
        """
        Check if the MSB has a valid value
        """
        if not 11 <= msb<= 29:
                raise ValueError(
                    "The most significant bit cannot be bigger than 29 or smaller than 11")
    def _check_can_enc(self,lsb,value:int,msb:Union[int,None]=None)->None:
        """
        Checks if the next value to be encoded in the same word, can be encoded without
        rewritting values already encoded
        """
        b_count = 1 if value==0 else value.bit_count()
        pos2 = lsb+ b_count -1 # Relative position
        if msb is not None:
            pos2 = msb

        if (self.a429vals[-1].lsb< lsb<self.a429vals[-1].msb)or \
                (self.a429vals[-1].lsb< pos2<self.a429vals[-1].msb):
            raise ValueError(f"You cannot encode between {lsb} and {pos2} because there is osmething encoded between {self.a429vals[-1].lsb} and {self.a429vals[-1].msb} already")
        
    def _check_lsb(self,lsb):
        if not 9 <= lsb <= 29:
            raise ValueError(
                "The least significant bit cannot be bigger than 29 or smaller than 9"
            )
    def _check_encoded(self):
        """
        Check if there are any encoded ARINC429 values.
        
        Raises:
            ValueError: If no values have been encoded yet.
        """
        if not self.a429vals:
            raise ValueError("Can't add any values to uninitialized encoders")
    def add_bnu(self,value:int,pos:int):
        """
        Add a BNU (Binary Unsigned) encoded value to your A429 word.

        Args:
            value (int): The unsigned binary value to encode
            pos (int): The bit position where the value should be placed (9-29)(LSB)

        Raises:
            ValueError: If the position is invalid or if the value would overlap with existing encoded data
        """
        self._check_msb(pos)
        self._check_can_enc(pos,value)
        self._check_encoded()

        byte1 = self.a429vals[-1].byte1
        byte2 = self.a429vals[-1].byte2
        byte3 = self.a429vals[-1].byte3
        byte4 = self.a429vals[-1].byte4
        byte4 &= ~(1 << 7) # Clear the parity bit

        data = (byte4 << 24) | (byte3<<16) | (byte2<<8) | byte1
        width = max(1, value.bit_length())
        mask  = (1 << width) - 1
        data &= ~(mask << (pos - 1))
        data= data| ((value& mask) << (pos - 1))

        byte1 = data & 0xFF
        byte2 = (data >> 8) & 0xFF
        byte3 = (data >> 16) & 0xFF
        byte4 = (data >> 24) & 0xFF

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))
        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        word = ArincWord(label=self.a429vals[-1].label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding="BNU",
                         msb=pos+width,
                         lsb=pos,
                         sdi=self.a429vals[-1].sdi,
                         ssm=self.a429vals[-1].ssm,
                         value=value,
                         offset=None,
                         scale=None,
                         data=data)
        self.a429vals.append(word)

    def add_bnr(self,value:Union[int,float],lsb:int,msb:int,scale:float=1.,offset:float=0.)->None:
        """
        Add a BNR encoded value to the word.
        """
        self._check_msb(msb)
        self._check_can_enc(lsb,int(value),lsb)
        self._check_encoded()

        byte1 = self.a429vals[-1].byte1
        byte2 = self.a429vals[-1].byte2
        byte3 = self.a429vals[-1].byte3
        byte4 = self.a429vals[-1].byte4
        byte4 &= ~(1 << 7) # Clear the parity bit

        cval = (value -offset)/scale
        cval= int(cval) << (lsb-1)
        data = (byte4 << 24) | (byte3<<16) | (byte2<<8) | byte1
        data = data +cval
        

        byte1 = data & 0xFF
        byte2 = (data >> 8) & 0xFF
        byte3 = (data >> 16) & 0xFF
        byte4 = (data >> 24) & 0xFF

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))
        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        word = ArincWord(label=self.a429vals[-1].label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding="BNR",
                         msb=msb,
                         lsb=lsb,
                         sdi=self.a429vals[-1].sdi,
                         ssm=self.a429vals[-1].ssm,
                         value=value,
                         offset=offset,
                         scale=scale,
                         data=data)
        self.a429vals.append(word)



    def add_dsc(self,value:int,pos:int):
        """
        Add a DSC (Discrete) encoded value to your A429 word.

        Args:
            value (int): The unsigned binary value to encode
            pos (int): The bit position where the value should be placed (9-29)(LSB)

        Raises:
            ValueError: If the position is invalid or if the value would overlap with existing encoded data
        """
        self._check_msb(pos)
        self._check_can_enc(pos,value)
        self._check_encoded()

        byte1 = self.a429vals[-1].byte1
        byte2 = self.a429vals[-1].byte2
        byte3 = self.a429vals[-1].byte3
        byte4 = self.a429vals[-1].byte4
        byte4 &= ~(1 << 7) # Clear the parity bit

        data = (byte4 << 24) | (byte3<<16) | (byte2<<8) | byte1
        width = max(1, value.bit_length())
        mask  = (1 << width) - 1
        data &= ~(mask << (pos - 1))
        data= data| ((value& mask) << (pos - 1))

        byte1 = data & 0xFF
        byte2 = (data >> 8) & 0xFF
        byte3 = (data >> 16) & 0xFF
        byte4 = (data >> 24) & 0xFF

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))
        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        word = ArincWord(label=self.a429vals[-1].label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding="BNU",
                         msb=pos+width,
                         lsb=pos,
                         sdi=self.a429vals[-1].sdi,
                         ssm=self.a429vals[-1].ssm,
                         value=value,
                         offset=None,
                         scale=None,
                         data=data)
        self.a429vals.append(word)

        
    @property
    def word(self) -> int:
        return self.a429vals[-1].word

    @property
    def bword(self) -> bytes:
        return self.a429vals[-1].get_bytes()

    def _can_bnr(self,msb,lsb,data)->None:
        """
        Check if the value can be encoded in the BNR range 
        """

        nbits = int(data).bit_length()
        if nbits > msb - lsb:
            raise ValueError(
                f"Value {data} requires {nbits} bits. It cannot fit in the range {msb} to {lsb}"
            )


    def _encode_bnr(self,encoding,label,msb,lsb,sdi,ssm,scale,offset,value):
        """
        Encode following the BNR schema

        data = (value - offset) / offset
        """
        data = (value - offset) / scale
        self._can_bnr(msb,lsb,data)

        # Byte1 - label
        byte1 = reverse_label(label)
        mov = 2

        if lsb > 11:
            data = int(data) << (lsb - 11)

        elif lsb < 11:
            data = int(data) >> (11 - lsb)

        byte2 = sdi
        byte2 |= (int(data)) << mov
        byte2 &= 0xFF
        # Byte 3: Data
        byte3 = 0
        byte3 |= int(data) >> (mov + 4)
        byte3 &= 0xFF
        

        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(data) >> (mov + 12)) & 0x3F
        byte4 |= ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80


        word = ArincWord(label=label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=encoding,
                         msb=msb,
                         lsb=lsb,
                         sdi=sdi,
                         ssm=ssm,
                         value=value,
                         offset=offset,
                         scale=scale,
                         data=data)
        self.a429vals.append(word)

    def _msb_mask(self, msb) -> int:
        masks = {
            # byte
            28: 0b1110111,
            27: 0b1110011,
            26: 0b1110001,
            25: 0b1110000,
            # Byte3
            24: 0b0111111,
            23: 0b0011111,
            22: 0b0001111,
            21: 0b0000111,
            20: 0b0000011,
            19: 0b0000001,
            18: 0b0000000,
            # Byte2
            17: 0b0111111,
            16: 0b0011111,
            15: 0b0000111,
            14: 0b0000011,
            13: 0b0000001,
            12: 0b0000001,
            11: 0b0000000,
        }

        return masks[msb]

    def reset(self):
        """
        Reset the encoder to the initial state
        """
        self.a429vals = []

    def _encode_bcd(self,encoding:str,label:int,sdi:int,ssm:int,value:int):
        """
        BCD encoding for arinc429 data
        """
        mov = 2  # We dont care about MSB or LSB for BCD
        if value < 0:
            raise ValueError(
                "BCD encoding does not support negative values. Use BNR encoding instead."
            )

        data = value
        if value > 79999:  # Cant encode antyhing bigger than this
            data = data // 10
        # Encode data for BCD
        iterval = int(data)
        i = 0
        encVal = 0
        while iterval > 0:
            encVal |= (iterval % 10) << (4 * i)
            iterval //= 10
            i += 1
        data = encVal
        # Normal encoding process
        # Byte 1
        byte1 = reverse_label(label)

        # Byte 2
        byte2 = sdi
        byte2 |= (int(data) & 0x3F) << mov
        byte2 &= 0xFF

        # Byte 3: Data
        byte3 = 0
        byte3 |= int(data) >> (mov + 4)
        byte3 &= 0xFF
        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(data) >> (mov + 12)) & 0x3F
        byte4 |= ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80


        word = ArincWord(label=label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=encoding,
                         msb=None,
                         lsb=None,
                         sdi=sdi,
                         ssm=ssm,
                         value=value,
                         offset=None,
                         scale=None,
                         data=data)
        self.a429vals.append(word)




    def _encode_dsc(self,encoding:str,label:int,msb:int,lsb:int,sdi:int,ssm:int,value:int):
        """
        DSC encoding for arinc429 data
        """
        mov = 2
        data = int(value)
        if (data.bit_length() > ((msb - lsb)+1)):
            raise ValueError(f"You need more bits in the word to encode your binary value: {bin(data)}")
        
        data = int(value) << (lsb - 11)
        #breakpoint()

        # Encode data for DSC
        # Byte 1
        byte1 = reverse_label(label)

        # Byte 2
        byte2 = sdi
        byte2 |= (int(data) & 0x3F) << mov
        byte2 &= 0xFF

        # Byte 3: Data
        byte3 = 0
        byte3 |= int(data) >> (mov + 4)
        byte3 &= 0xFF
        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(data) >> (mov + 12)) & 0x3F
        byte4 |= ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        word = ArincWord(label=label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=encoding,
                         msb=msb,
                         lsb=lsb,
                         sdi=sdi,
                         ssm=ssm,
                         value=value,
                         offset=None,
                         scale=None,
                         data=data)
        self.a429vals.append(word)


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
            num_ones += bin(byte).count("1")

        return num_ones % 2 == 0

