from arinc429.common import ArincWord,reverse_label



def test_ArincWord():
    w = ArincWord(byte4=0x10,byte3=0x20,byte2=0x30,byte1=0x40)
    assert w.word == 0x10203040
    assert w.get_bytes() == bytes([0x10, 0x20, 0x30, 0x40])

def test_reverse_label():
    label = 0o101
    assert reverse_label(label) == 0b10000010
