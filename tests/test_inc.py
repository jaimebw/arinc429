import pytest
from src import Arinc429Encoder




def test_no_encoding_input():
    enc = Arinc429Encoder()
    with pytest.raises(ValueError):
        enc.encode()

def test_no_compataible_sdi():
    enc = Arinc429Encoder()
    with pytest.raises(ValueError):
        enc.encode(sdi = 1000, encoding= "BNR")

def test_no_compataible_ssm():
    enc = Arinc429Encoder()
    with pytest.raises(ValueError):
        enc.encode(ssm= 5, encoding= "BNR")

def test_no_compataible_msb():
    enc = Arinc429Encoder()
    with pytest.raises(ValueError):
        enc.encode(msb= 30, encoding= "BNR")

def test_no_compataible_lsb():
    enc = Arinc429Encoder()
    with pytest.raises(ValueError):
        enc.encode(lsb= 30, encoding= "BNR")

