from arinc429 import Encoder

def test_enc_bnr_zero():
    a429 = Encoder()
    a429.encode(encoding="BNR")
    assert(a429.bword== b"\x80\x00\x00\x00")

def test_enc_brn_cases():
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

    det={
            "label":0o206,
            "value":105,
            "ssm": 0x01,
            "sdi":0,
            "encoding":"BNR"
            }

    a429.encode(**det)
    assert(a429.bword== b"\xa0\x01\xa4\x61")

    

