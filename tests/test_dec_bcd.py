from arinc429 import Decoder
import pytest


def test_dec_bcd_zero():
    a429 = Decoder()
    word = a429.decode(
        b"\x80\x00\x00\x00",
        encoding="BCD",
    )
    assert word.label == 0o000
    assert word.ssm == 0x00
    assert word.sdi == 0
    assert word.value == 0


def test_dec_bcd_case1():
    a429 = Decoder()
    word = a429.decode(
        b"\xfe\x14\x04\xa1",
        encoding="BCD",
    )
    assert word.label == 0o205
    assert word.ssm == 0x03
    assert word.sdi == 0
    assert word.value == 78501


def test_dec_bcd_case2_sdi():
    a429 = Decoder()
    word = a429.decode(
        b"\x62\x00\x01\x61",
        encoding="BCD",
    )
    assert word.label == 0o206
    assert word.ssm == 0x03
    assert word.sdi == 1
    assert word.value == 8000


@pytest.mark.parametrize(
    "payload,label,ssm,sdi,value",
    [
        (b"\x24\x8d\x16\xca", 0o123, 0x01, 2, 12345),
        (b"\x00\x00\x1c\xff", 0o377, 0x00, 0, 7),
        (b"\xd4\x00\x03\x15", 0o250, 0x02, 3, 50000),
        (b"\xe2\x66\x65\xa7", 0o345, 0x03, 1, 9999),
        (b"\xa4\x8d\x14\x22", 0o104, 0x01, 0, 12345),
    ],
)
def test_dec_bcd_more_cases(payload, label, ssm, sdi, value):
    a429 = Decoder()
    word = a429.decode(
        payload,
        encoding="BCD",
    )
    assert word.label == label
    assert word.ssm == ssm
    assert word.sdi == sdi
    assert word.value == value
