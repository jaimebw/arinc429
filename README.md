# Arinc 429

## How to install

```bash
pip install arinc429
```

## Examples
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
        "label":0o205, # Same label as before
        "value":1, # 1 or 0 as it is DSC
        "msb":11, # We dont care about lsb
        "encoding":"DSC"
        }
a429.encode(**det)
a429.encode(**w2)
word = a429.word # uint32_t word


```
This API is subject to change.

If you want to encode another value using the same encoder, you need to reset the encoder before.
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
The encoder takes care so you dont shoot your foot while encoding and loosing information,
it wont let you encode something into a value that is already being used. 

If you were to try use a different msb in the add_dsc method, it would raise an exception as all the bits are already being used.

This wont apply to multiple DSC values, so you can rewrite the DSC values


## Roadmap

* [x] Encode BNR 
* [x] Encode BCD 
* [ ] Encode DSC 
* [ ] Raw encoding ( label + value)
* [ ] Mixed encoding (DSC + BNR)

* [ ] Decode BNR
* [ ] Decode rest of stuff

* [ ] Implement in C

I dont really follow a specific roadmap, I just add features as I need them. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Other stuff

As for docs, I think the API is pretty simple and self-explanatory. If you have any questions, feel free to ask. 

## Change log

* v0.1.1 - Added BCD encoding

* v0.1.0 - Initial release (encode BNR)


## Documentation

## Technical Overview

This library provides comprehensive support for encoding and decoding ARINC 429 data words. ARINC 429 is a widely used avionics data bus specification that defines how avionics systems communicate in commercial aircraft.

### Supported Encodings

The library currently supports or plans to support the following encoding formats:

- Binary (BNR)
- Binary Coded Decimal (BCD)
- Discrete (DSC)
- Hybrid formats (e.g., BNR + DSC combinations)
- Raw encoding (custom label + value pairs)

### Flexible Implementation

The library is designed to be flexible and extensible, allowing for:

- Standard ARINC 429 word formats
- Custom data encoding schemes
- Direct manipulation of label and data fields
- Support for various SSM (Sign/Status Matrix) configurations

For specific encoding requirements or custom implementations, please refer to the examples section above.

