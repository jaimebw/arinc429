from arinc429 import Decoder, ArincWord
import pytest


def test_dec_bnr_zero():
    a429 = Decoder()
    word = a429.decode([0,0,0,0], 
                encoding="BNR",
                )
    assert(word.value == 0)
def test_dec_bnr_std():
    a429 = Decoder()
    word = a429.decode(
           b"\xe0\x01\x90\xa1",
                encoding="BNR",
                )
    assert(word.label== 0o205)
    assert(word.ssm== 0x03)
    assert(word.sdi== 0)
    assert(word.value == 100)

def test_dec_bnr_ssm1():
    a429 = Decoder()
    word = a429.decode(
                b"\xa0\x01\xa4\x61",
                encoding="BNR",
                )
    assert(word.label== 0o206)
    assert(word.ssm== 0x01)
    assert(word.sdi== 0)
    assert(word.value == 105)

def test_dec_brn_msb_lsb():
    a429 = Decoder()
    word = a429.decode(
            b"\x60\x0c\x80\x8b",
                encoding="BNR",
                lsb = 15
                )
    assert(word.label== 0o321)
    assert(word.ssm== 0x03)
    assert(word.sdi== 0)
    assert(word.value == 50)

def test_dec_brn_msb_lsb2():
    a429 = Decoder()
    word = a429.decode(
            b"\x60\x3F\x80\xdb",
                encoding="BNR",
                lsb =16 ,
                
                )
    assert(word.label== 0o333)
    assert(word.ssm== 0x03)
    assert(word.sdi== 0)
    assert(word.value == 127)


