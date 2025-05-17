from arinc429 import Encoder


def test_enc_bcd_zero():
    a429 = Encoder()
    a429.encode(encoding="BCD")
    assert a429.bword== b"\x80\x00\x00\x00"
    assert a429.word== 0x80000000

def test_enc_bcd_case1():
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
    assert(a429.word== 0xfe1404a1)

def test_enc_bcd_case2():
    a429 = Encoder()
    det={
            "label":0o206,
            "value":80001,
            "ssm": 0x03,
            "sdi":0,
            "encoding":"BCD"
            }
    a429.encode(**det)
    assert a429.bword== b"\xe2\x00\x00\x61"
    assert a429.word== 0xe2000061

def test_enc_bcd_case3():
    a429 = Encoder()
    det={
            "label":0o206,
            "value":80001,
            "ssm": 0x03,
            "sdi":1,
            "encoding":"BCD"
            }
    a429.encode(**det)
    assert a429.bword== b"\x62\x00\x01\x61"
    assert a429.word== 0x62000161
