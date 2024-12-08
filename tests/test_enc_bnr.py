from arinc429 import Encoder
import pytest

def test_enc_bnr_zero():
    a429 = Encoder()
    a429.encode(encoding="BNR")
    assert(a429.bword== b"\x80\x00\x00\x00")

def test_enc_brn_std():
    a429 = Encoder()
    det={
            "label":0o205,
            "value":100,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"BNR"
            }
    a429.encode(**det)
    assert(a429.bword== b"\xe0\x01\x90\xa1")

def test_enc_brn_ssm1():
    a429 = Encoder()
    det={
            "label":0o206,
            "value":105,
            "ssm": 0x01,
            "sdi":0,
            "encoding":"BNR"
            }
    a429.encode(**det)
    assert(a429.bword== b"\xa0\x01\xa4\x61")

def test_enc_brn_msb_lsb():
    a429 = Encoder()
    det={
            "label":0o321,
            "value":50,
            "ssm": 0x03,
            "sdi":0,
            "msb": 25,
            "lsb": 15,
            "encoding":"BNR"
            }
    a429.encode(**det)
    assert(a429.bword== b"\x60\x0c\x80\x8b")

def test_enc_brn_msb_lsb2():
    a429 = Encoder()
    det={
            "label":0o333,
            "value":127.7,
            "ssm": 0x03,
            "sdi":0,
            "msb": 23,
            "lsb": 16,
            "encoding":"BNR"
            }
    a429.encode(**det)
    assert(a429.bword== b"\x60\x3F\x80\xdb")

def test_enc_brn_msb_not_enough_bits():
    a429 = Encoder()
    det={
            "label":0o333,
            "value":127.7,
            "ssm": 0x03,
            "sdi":0,
            "msb": 21,
            "lsb": 16,
            "encoding":"BNR"
            }
    with pytest.raises(ValueError):
        a429.encode(**det)
# TODO: Implement test_enc_bnr_msb_lsb_more_info_no_sdi
@pytest.mark.skip(reason="Not implemented")
def test_enc_bnr_msb_lsb_more_info_no_sdi():
    a429 = Encoder()
    det={
            "label":0o110,
            "value":42.2431231,
            "ssm": 0x03,
            "sdi":0,
            "msb": 29,
            "lsb": 9,
            "scale":1,
            "offset":0,
            "encoding":"BNR"
            }
    a429.encode(**det)
    assert(a429.bword== b"\x60\x3F\x80\xdb")

