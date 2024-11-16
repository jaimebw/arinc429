# Arinc 429

## How to install

```bash
pip install arinc429
```

## Examples
```
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
    word = a429.word
    bin_vals = a429.b_arr

```
## Roadmap

1. Encode DSC
2. Encode BCD
3. Mixed encoding (DSC + BNR)

4. Decode BNR
4. Decode ..


5. Implement in C





