# MacTools

MacTools is a MAC-centric library for aiding in network handling and automation.

Full test coverage and fully type annoted.

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

# returns the MAC without an delimiters or spaces (001122AABBCC)
mac.clean

# returns the MAC with period delimiters (0011.22AA.BBCC)
mac.period

# returns the decimal/numeric form (73596058572)
mac.decimal

# returns the OUI (00:11:22)
mac.oui
```

The full format list includes: clean, colon, period, hyphen, space, oui,
decimal, binary

#### IPv6 Support

This library has some methods for simplifying IPv6 SLAAC-based address creation:

```python
# returns the IPv6 Suffix/Interface ID in EUI-64 per RFC 4291 (0211:22ff:feaa:bbcc)
mac.eui64_suffix

# returns the Link-local address (fe80::0211:22ff:feaa:bbcc)
mac.link_local_address

# returns a Global Unicast Address (2001:db8::) as `ipaddress.IPv6Address`
mac.get_global_address('2001:db8::0211:22ff:feaa:bbcc')
```

### OUICache

Local cache of the IEEE OUI MA-L, MA-M, and MA-S registries for quick look-ups without needing to
consistently hit API endpoints for individual queries.

`MacAddress` currently automatically performs the look-up on creation.

The full information is available, including OUI, Vendor, Address, etc.

The cache also contains specific references to commonly defined non-vendor OUIs
such as Multicast, IEEE protocols (STP, LLDP, etc), Locally administered and others.

#### Usage

Intakes a string MAC/OUI or `MacAddress` object for either vendor or full record
from the IEEE OUI MA-L registry.  The cache will be built if one is not present
(or if manually prompted) or the version of the code has changed.

```python
from mactools import get_oui_cache

# the `mac` defined above already has the look-up performed and recorded on creation, if the record was found

vendor = mac.vendor

cache = get_oui_cache()
oui = '01000C'

# These methods would also work with the `mac` defined above as well 
vendor = cache.get_vendor(oui)
```

`vendor` will be the string of vendor registered to IEEE.
It will also identify common protocol MACs (such as Spanning Tree, Cisco/Extreme, etc.) and randomized MACs (locally administered).

## License

This project is under the MIT license (see the LICENSE file for full text).