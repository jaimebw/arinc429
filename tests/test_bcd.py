from arinc429 import Encoder
import pytest


@pytest.mark.skip
def test_enc_bcd_zero():
    a429 = Encoder()
    a429.encode(encoding="BCD")
    assert(a429.bword== b"\x80\x00\x00\x00")

def test_enc_bcd_cases():
    a429 = Encoder()

    det={
            "label":0o205,
            "value":78501,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"BCD"
            }
    a429.encode(**det)
    assert(a429.bword== b"\xfe\x14\x04\xa1")
    det={
            "label":0o206,
            "value":80001,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"BCD"
            }
    a429.encode(**det)
    assert(a429.bword== b"\xe2\x00\x00\x61")
    det={
            "label":0o206,
            "value":80001,
            "ssm": 0x03,
            "sdi":1,
            "encoding":"BCD"
            }
    a429.encode(**det)
    assert(a429.bword== b"\x62\x00\x01\x61")
