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

```
## Roadmap

* [x] Encode BCD 
* [ ] Encode DSC 
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

v0.1.1 - Added BCD encoding
v0.1.0 - Initial release (encode BNR)


