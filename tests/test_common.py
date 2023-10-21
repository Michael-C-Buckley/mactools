# Common Test Library

# Python Modules
from dataclasses import dataclass
from random import randint
from typing import Literal

# Local Modules
from mactools.macaddress import (
    MacAddress,
    Notation
)

from mactools.oui_cache.oui_classes import (
    OUICache,
    OUIRecord
)

TEST_IEEE_DATA = {
    'oui': '6026AA',
    'vendor': 'Cisco Systems, Inc',        
    'hex_oui': '60-26-AA',
    'street_address': '80 West Tasman Drive',
    'city': 'San Jose',
    'state': 'CA',
    'postal_code': '94568',
    'country': 'US'
}

TEST_OUI_STRING = '6026aa'
TEST_RECORD = OUIRecord(**TEST_IEEE_DATA)
TEST_CACHE = OUICache({TEST_OUI_STRING.upper(): TEST_RECORD})

OUI_CORE_PATH = 'mactools.oui_cache.oui_core'
OUI_CLASSES_PATH = 'mactools.oui_cache.oui_classes'

@dataclass
class TestMac:
    mac: str
    binary: int
    decimal: int


# Fixed, Reusable Test Cases
SAMPLE_EUI48 = TestMac('60:26:AA:BB:99:CC',
    11000000010011010101010101110111001100111001100,
    105719189445068)

SAMPLE_EUI64 = TestMac('00:11:AA:00:00:BB:99:DD',
    10001101010100000000000000000101110111001100111011101,
    4971991593097693)

MAC48 = MacAddress(SAMPLE_EUI48.mac)
MAC64 = MacAddress(SAMPLE_EUI64.mac)

def create_random_hex_bit():
    """
    Returns a single bit between 0-9 or A-F
    """
    return hex(randint(0, 15))[2:3].upper()

def create_random_hex_string(length: int = 2):
    """
    Returns a hex string of specified length
    """
    bit_list = [create_random_hex_bit() for _ in range(length)]
    return ''.join(bit_list)

def create_random_mac(eui: Literal[48, 64] = 48, delimiter: Notation = Notation.COLON):
    """
    Returns a valid random MAC address
    """
    eui = int(eui)
    if eui not in [48, 64]:
        raise ValueError('EUI might be either `48` or `64`')

    hex_length = 4 if delimiter == Notation.PERIOD else 2
    segments = eui/(4*hex_length)
    
    mac_portions = [create_random_hex_string(hex_length) for _ in range(int(segments))]
    return delimiter.value.join(mac_portions)
