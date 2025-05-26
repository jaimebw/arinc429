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
        # General stuff
        self.data: Union[int, float] = 0
        self.label: int = 0
        self.sdi: int = 0
        self.ssm: int = 0
        self.value: Union[int, float] = 0
        self.encoding: str = ""
        self.msb: int = 29
        self.lsb: int = 11
        self.encodings: List[str] = []  # List of encodings used
        # BRN encoding
        self.offset: Union[int, float] = 0
        self.scale: Union[int, float] = 1
        # Output stuff
        self.word_val: int = 0
        self.b_arr_val: bytes = b"0"
        # we will use this if more than one encoding is used
        self.word_list: List[int] = []
        self.blist: List[bytes] = []
        # Byte list in int
        self.a429vals: List[ArincWord] = []

    def __repr__(self) -> str:
        return '\n'.join([str(word) for word in self.a429vals])

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
        self.value = value
        self.label = label
        self.sdi = sdi
        self.ssm = ssm
        self.encoding = encoding
        self.msb = msb
        self.lsb = lsb
        self.offset = offset
        self.scale = scale
        # Check if the input is valid
        self._check_sdi()
        self._check_ssm()
        self._check_msb()
        self._check_lsb()

        if self.encoding == "BNR":
            self._encode_bnr()
        elif self.encoding == "BCD":
            self._encode_bcd()
        elif self.encoding == "DSC":
            self._encode_dsc()
        else:
            raise ValueError(f"Encoding {self.encoding} not supported")

        self._add_encoding(self.encoding)

    def _check_sdi(self):
        if not 0 <= self.sdi <= 0x03:
            raise ValueError("The SDI cannot be negative or bigger than 0x03")
        if self.lsb < 11 and self.sdi != 0:
            raise ValueError("SDI must be 0 if LSB is smaller than 11")

    def _check_ssm(self):
        if not 0 <= self.ssm <= 0x03:
            raise ValueError("The SSM cannot be negative or bigger than 0x03")

    def _check_msb(self,msb:Union[None,int]=None):
        if msb: #use the method somewhere else
            if not 11 <= msb <= 29:
                raise ValueError(
                    "The most significant bit cannot be bigger than 29 or smaller than 11")


        if not 11 <= self.msb <= 29:
            raise ValueError(
                "The most significant bit cannot be bigger than 29 or smaller than 11"
            )
    def _check_can_enc_dsc(self,msb)->None:
        if self.lsb < msb <self.msb:
            raise ValueError("DSC encoding can only be used out of the used range")
        

    def _check_lsb(self):
        if not 9 <= self.lsb <= 29:
            raise ValueError(
                "The least significant bit cannot be bigger than 29 or smaller than 9"
            )

    def add_dsc(self,value:int,msb:int):
        """
        Add a DSC encoded value to your A429 word
        """
        if not self.a429vals:
            raise ValueError("You need to encode a value first before adding DSC values. Use the encode method")
        self._add_encoding("DSC")
        self._check_msb(msb)
        self._check_can_enc_dsc(msb)

        byte1 = self.a429vals[-1].byte1
        byte2 = self.a429vals[-1].byte2
        byte3 = self.a429vals[-1].byte3
        byte4 = self.a429vals[-1].byte4

        byte4 &= 0x80 # Clear the parity bit

        if msb <17:
            byte2 = (byte2& ~(1 << 16- msb)) | (value<< 16- msb)
        elif msb <25:
            byte3 = (byte3& ~(1 << 24- msb)) | (value<< 24- msb)
        else:
            byte4 = (byte4& ~(1 << 29- msb)) | (value<< 29- msb)

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))
        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        self.a429vals[-1].byte2 = byte2
        self.a429vals[-1].byte3 = byte3
        self.a429vals[-1].byte4 = byte4
        self.a429vals[-1].encoding += " & DSC"
        self._build_word(byte4,byte3,byte2,byte1)
        
    @property
    def word(self) -> int:

        return self.word_val

    @property
    def bword(self) -> bytes:
        return self.a429vals[-1].get_bytes()

    def _can_bnr(self)->None:
        """
        Check if the value can be encoded in the BNR range 
        """

        nbits = int(self.data).bit_length()
        if nbits > self.msb - self.lsb:
            raise ValueError(
                f"Value {self.data} requires {nbits} bits. It cannot fit in the range {self.msb} to {self.lsb}"
            )


    def _encode_bnr(self):
        """
        Encode following the BNR schema

        data = (value - offset) / offset
        """
        self.data = (self.value - self.offset) / self.scale
        self._can_bnr()

        # Byte1 - label
        byte1 = self._reverse_label(self.label)
        mov = 2
        # Byte2 - SDI + some word stuff

        if self.lsb > 11:
            self.data = int(self.data) << (self.lsb - 11)

        elif self.lsb < 11:
            self.data = int(self.data) >> (11 - self.lsb)

        byte2 = self.sdi
        byte2 |= (int(self.data)) << mov
        byte2 &= 0xFF
        # Byte 3: Data
        byte3 = 0
        byte3 |= int(self.data) >> (mov + 4)
        byte3 &= 0xFF
        

        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(self.data) >> (mov + 12)) & 0x3F
        byte4 |= self.ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80


        word = ArincWord(label=self.label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=self.encoding,
                         msb=self.msb,
                         lsb=self.lsb,
                         sdi=self.sdi,
                         ssm=self.ssm,
                         value=self.value,
                         offset=self.offset,
                         scale=self.scale,
                         data=self.data)
        self.a429vals.append(word)
        self._build_word(byte4,byte3,byte2,byte1)

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
        self.data = 0
        self.label = 0
        self.sdi = 0
        self.ssm = 0
        self.value = 0
        self.encoding = ""
        self.msb = 29
        self.lsb = 11
        self.encodings = []
        self.a429vals = []

    def _encode_bcd(self):
        """
        BCD encoding for arinc429 data
        """
        mov = 2  # We dont care about MSB or LSB for BCD
        if self.value < 0:
            raise ValueError(
                "BCD encoding does not support negative values. Use BNR encoding instead."
            )

        self.data = self.value
        if self.value > 79999:  # Cant encode antyhing bigger than this
            self.data = self.data // 10
        # Encode data for BCD
        iterval = int(self.data)
        i = 0
        encVal = 0
        while iterval > 0:
            encVal |= (iterval % 10) << (4 * i)
            iterval //= 10
            i += 1
        self.data = encVal
        # Normal encoding process
        # Byte 1
        byte1 = self._reverse_label(self.label)

        # Byte 2
        byte2 = self.sdi
        byte2 |= (int(self.data) & 0x3F) << mov
        byte2 &= 0xFF

        # Byte 3: Data
        byte3 = 0
        byte3 |= int(self.data) >> (mov + 4)
        byte3 &= 0xFF
        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(self.data) >> (mov + 12)) & 0x3F
        byte4 |= self.ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80


        # self.word_list.append(self.word_val)
        # self.blist.append(self.b_arr_val)

        word = ArincWord(label=self.label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=self.encoding,
                         msb=None,
                         lsb=None,
                         sdi=self.sdi,
                         ssm=self.ssm,
                         value=self.value,
                         offset=None,
                         scale=None,
                         data=self.data)
        self.a429vals.append(word)
        self._build_word(byte4,byte3,byte2,byte1)


    def _add_encoding(self, encoding: str) -> None:
        """
        Add an encoding to the list of previous encodings
        """
        # Making sure that only one BNR or BCD encoding is present

        if "BNR" in self.encodings or "BCD" in self.encodings:
            raise ValueError("Only one BNR or BCD encoding is allowed per word")

        self.encodings.append(encoding)

    def _encode_dsc(self):
        """
        DSC encoding for arinc429 data
        """
        mov = 2
        data = int(self.value)
        if (data.bit_length() > ((self.msb - self.lsb)+1)):
            raise ValueError(f"You need more bits in the word to encode your binary value: {bin(data)}")
        
        self.data = int(self.value) << (self.lsb - 11)
        #breakpoint()

        # Encode data for DSC
        # Byte 1
        byte1 = self._reverse_label(self.label)

        # Byte 2
        byte2 = self.sdi
        byte2 |= (int(self.data) & 0x3F) << mov
        byte2 &= 0xFF

        # Byte 3: Data
        byte3 = 0
        byte3 |= int(self.data) >> (mov + 4)
        byte3 &= 0xFF
        # Byte 4- Data + SSM + Parity
        byte4 = 0
        byte4 |= (int(self.data) >> (mov + 12)) & 0x3F
        byte4 |= self.ssm << 5

        parity = self._get_parity(bytes([byte1, byte2, byte3, byte4]))

        if parity:  # If not, the parity is already set to zero
            byte4 |= 0x80

        word = ArincWord(label=self.label,
                         byte1=byte1,
                         byte2=byte2,
                         byte3=byte3,
                         byte4=byte4,
                         encoding=self.encoding,
                         msb=None,
                         lsb=None,
                         sdi=self.sdi,
                         ssm=self.ssm,
                         value=self.value,
                         offset=None,
                         scale=None,
                         data=self.data)
        self.a429vals.append(word)
        self._build_word(byte4,byte3,byte2,byte1)


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

    def _reverse_label(self, label: int) -> int:
        self.rlabel = reverse_label(label)
        return self.rlabel

    @property
    def data_val(self) -> Union[int, float]:
        """
        Return the value of the processed value to be encoded
        """
        return self.data

    def _build_word(self,byte4,byte3,byte2,byte1):
        """
        Build the arinc429 32 bite word form the invidivual bytes
        """
        self.word_val = (byte4<<24) | (byte3<<16) | (byte2<<8) | byte1

