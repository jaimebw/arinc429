# PyArinc 429

[![PyPI version](https://img.shields.io/pypi/v/arinc429.svg)](https://pypi.org/project/arinc429/)
[![Build Status](https://github.com/jaimebw/arinc429/actions/workflows/run-tests.yml/badge.svg)](https://github.com/jaimebw/arinc429/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/arinc429.svg)](https://pypi.org/project/arinc429/)

Note: The API is subject to change! The encoder is working the decoder is close to working!

PRs accepted!


## How to install

```bash
pip install arinc429
```
This lib has zero dependecies (and it will stay this way!)

## How to use

### Encoder

```python
from arinc429 import Encoder 
a429 = Encoder()
det= {
        "label":0o205,
        "value":100,
        "ssm": 0x03,
        "sdi":0,
        "encoding":"BNR"
        }
a429.encode(**det)
word = a429.word # uint32_t word
bin_vals = a429.bword # binary word
# Multiple words
a429 = Encoder()
w1= {
        "label":0o205,
        "value":100,
        "ssm": 0x03,
        "sdi":0,
        "msb":29,
        "lsb":12
        "encoding":"BNR"
        }
w2= {
        "value":1, 
        "msb":11, # Bit position
        }
a429.encode(**det)
a429.add_dsc(**w2)
word = a429.word # uint32_t word


```

If you want to encode another label using the same encoder, you need to reset the encoder before.
```python
from arinc429 import Encoder 
a429 = Encoder()
det= {
        "label":0o205,
        "value":100,
        "ssm": 0x03,
        "sdi":0,
        "encoding":"BNR"
        }
a429.encode(**det)
det2= {
        "label":0o206,
        "value":100,
        "ssm": 0x03,
        "sdi":0,
        "encoding":"BNR"
        }
a429.reset() # If you dont do this, it will raise an exception 
a429.encode(**det)
```

In case you wan to encode a DSC value into a BNR word, you can do it like this:

```python
from arinc429 import Encoder 
a429 = Encoder()
det= {
        "label":0o205,
        "value":100,
        "ssm": 0x03,
        "sdi":0,
        "encoding":"BNR",
        "msb":28,
        }
a429.add_dsc(1,29) # Add a DSC value to the word
```
Same applies for BNU encoding with the ```add_bnu``` method and with BNR with the ```add_bnr``` method.

The encoder takes care so you dont shoot your foot while encoding and loosing information,
it wont let you encode something into a value that is already being used. 

If you were to try use a different msb in the add_dsc method, it would raise an exception as all the bits are already being used.

You can also acces the state of the word by slicing the objects:
```python
a429[0].word # will return the words first value when the first value was encoded
a429[-1].word # will return the words last value when the last value was encoded

```



### Container class

There is a container class that allows you to easily work with the Arinc429 words.
```python
from arinc429 import Arinc429Word

word = Arinc429Word(
    byte1=0x00,
    byte2=0x20,
    byte3=0x00,
    byte4=0xe1
)
```
It accepts multiple input formats and some cool helper functions like the ```visualize()``` method that will
output a string with a bit formatting of the word. Check src/common.py for more info.



### Decoder

This is WIP. Wont work sometimes...


```python
from arinc429 import Decoder
a429 = Decoder()
word = a429.decode(
            b"\xa0\x01\xa4\x61",
            encoding="BNR",
            )
assert(word.label== 0o206)
assert(word.ssm== 0x01)
assert(word.sdi== 0)
assert(word.value == 105)

```
## Roadmap

* [x] Encode BNR 
* [x] Encode BCD 
* [x] Encode DSC 
* [x] Encode BNU
* [x] Raw encoding ( label + value)
* [x] Mixed encoding (DSC + BNR)
* [x] Mixed encoding (BNU+ BNR)
* [x] Mixed encoding (DSC + DSC)
* [x] Mixed encoding (DSC + BNU)
* [x] Mixed encoding (BNR+ BNR)
* [ ] Encoding values with using the SDI/SSM as usable fields (Fun encodings)

* [X] Decode BNR
* [ ] Decode BCD
* [ ] Decode DSC
* [ ] Implement in C

I dont really follow a specific roadmap; I just add features as I need them.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Other stuff

As for docs, working on it... Feel free to do a PR to the docs branch

## Change log


* v0.1.6 - Add BNR + BNR, more test and general cleanup
* v0.1.5 - Corrected DSC encoding, added tests and added BNU encoding
* v0.1.4 - General bug correction
* v0.1.3 - Working BNR decoding
* v0.1.2 - Added BCD, DSC, BNR + DSC encoding
* v0.1.1 - Added BNR encoding
* v0.1.0 - Initial release (encode BNR)


## Technical Overview

This library provides comprehensive support for encoding and decoding ARINC 429 data words. 
ARINC 429 is a widely used avionics data bus specification that defines how avionics systems communicate in aircraft.

### Supported Encodings

The library currently supports or plans to support the following encoding formats:

- Binary (BNR)
- Binary Coded Decimal (BCD)
- Discrete (DSC)
- Binary Unsigned (BNU)
- Hybrid formats (e.g., BNR + DSC combinations)
- Raw encoding (custom label + value pairs)

### Flexible Implementation

The library is designed to be flexible and extensible, allowing for:

- Standard ARINC 429 word formats
- Custom data encoding schemes
- Direct manipulation of label and data fields
- Support for various SSM (Sign/Status Matrix) configurations

For specific encoding requirements or custom implementations, please refer to the examples section above.


"I steal fire not with torches, but with code. Not for men — but for the machines that do not dream yet."
