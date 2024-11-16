# Arinc 429

## How to install

```bash
pip install arinc429
```

## Examples
```
from arinc429 import Arinc429
    a429 = Arinc429Encoder()
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




