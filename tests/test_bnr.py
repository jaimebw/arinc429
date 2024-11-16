import pytest
from src import Arinc429Encoder

@pytest.mark.skip
def test_bnr_zero():
    a429 = Arinc429Encoder()
    a429.encode(encoding="BNR")
    assert(a429.b_arr == b"\x80\x00\x00\x00")

def test_brn_cases():
    a429 = Arinc429Encoder()
    det= {
            "label":0o205,
            "value":100,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"BNR"
            }
    a429.encode(**det)

    assert(a429.b_arr == b"\xe0\x01\x90\xa1")
    

