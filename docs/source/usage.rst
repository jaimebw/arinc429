Usage Guide
===========

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install arinc429

Install from source with test and docs dependencies:

.. code-block:: bash

   python -m pip install -e ".[dev,docs]"

Quick Example
-------------

Encode a BNR word and decode it back:

.. code-block:: python

   from arinc429 import Encoder, Decoder

   enc = Encoder()
   enc.encode(label=0o205, value=100, ssm=0x03, sdi=0, encoding="BNR")

   dec = Decoder()
   word = dec.decode(enc.bword, encoding="BNR")

   assert word.label == 0o205
   assert word.value == 100

Build Docs Locally
------------------

Generate HTML documentation:

.. code-block:: bash

   sphinx-build -b html docs/source docs/_build/html
