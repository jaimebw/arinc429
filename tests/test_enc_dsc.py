from arinc429 import Encoder




def test_enc_dsc_zero():
    a429 = Encoder()
    a429.encode(encoding="DSC")
    assert a429.word == 0x80000000

def test_enc_dsc_std():
    a429 = Encoder()
    det={
            "label":0o205,
            "value":1,
            "msb":27,
            "lsb":27,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"DSC"
            }
    a429.encode(**det)
    assert a429.bword == b"\xe4\00\00\xa1"
    a429.reset()
    det={
            "label":0o205,
            "value":1,
            "msb":29,
            "lsb":29,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"DSC"
            }
    a429.encode(**det)
    assert a429.bword == b"\xf0\00\00\xa1"
    a429.reset()
    det={
            "label":0o205,
            "value":1,
            "msb":17,
            "lsb":17,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"DSC"
            }
    a429.encode(**det)
    assert a429.bword == b"\xe0\x01\x00\xa1"
    assert a429.word == 0xE00100A1
    a429.reset()
    det={
            "label":0o205,
            "value":1,
            "msb":13,
            "lsb":13,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"DSC"
            }
    a429.encode(**det)
    assert a429.bword == b"\xe0\00\x10\xa1"
    assert a429.word == 0xE00010A1


def test_enc_dsc_bnu():
    """
    BNU is a fancy name to refer to encoding of binary values into multiple bits.
    For example, encoding an enum into 2 or more bits
    """
    a429 = Encoder()
    det={
            "label":0o205,
            "value":3,
            "msb":29,
            "lsb":28,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"DSC"
            }
    a429.encode(**det)
    assert a429.bword == b"\x78\00\00\xa1"
    assert a429.word == 0x780000A1
    pass


