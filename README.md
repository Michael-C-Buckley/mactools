# MacTools

MacTools is a MAC-centric library for aiding in network handling and automation.

## Installation

This is a publicly available library on PyPI and can be installed with:

`pip install mactools`

## Features

### MacAddress

MAC object similar to Python's `ipaddress` library.  Performs validation on
creation and allows quick and easy format changing for the user.  Accepts
EUI-48 and EUI-64 formats.

#### Usage

Built-in `MacAddress` attributes allow for conversion between the common formats
of either delimiters, decimal, or binary. Such as:

```python
from mactools import MacAddress
mac = MacAddress('00:11:22:AA:BB:CC')

# returns the MAC without an delimiters or spaces
mac.clean

# returns the MAC with period delimiters
mac.period

# returns the decimal/numeric form
mac.decimal

# returns the OUI
mac.oui
```

The full format list includes: clean, colon, period, hyphen, space, oui,
decimal, binary

### OUICache

Local cache of the IEEE OUI MA-L registry for quick look-ups without needing to
consistently hit API endpoints for individual queries.

The full information is available, including OUI, Vendor, Address, etc.

The cache also contains specific references to commonly defined non-vendor OUIs
such as Multicast, IEEE protocols (STP, LLDP, etc), and others.

#### Usage

Intakes a string MAC/OUI or `MacAddress` object for either vendor or full record
from the IEEE OUI MA-L registry.  The cache will be built if one is not present
(or if manually prompted) or the version of the code has changed.

```python
from mactools import get_oui_cache

cache = get_oui_cache()
oui = '01000C'

# These methods would also work with the `mac` defined above as well 
vendor = cache.get_vendor(oui)
record = cache.get_record(oui)
```

`vendor` will be the string of vendor registered to IEEE where `record` will be
an `OUIRecord` which includes all the information from IEEE.

## License

This project is under the MIT license (see the LICENSE file for full text).