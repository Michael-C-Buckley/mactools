# Common Test Library

# Python Modules
from dataclasses import dataclass
from re import search, compile, Match
from typing import Any
from unittest import TestCase

# Local Modules
from mactools import MacAddress

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


def test_regex_comparison(test_obj: TestCase, pattern: str, test_func: callable,
        test_samples: int, test_arg: Any = None):
    """
    Internal test method for testing to make sure it matches
    """
    test_regex = compile(pattern)
    if test_arg:
        test_list = [test_func(test_arg) for _ in range(test_samples)]
    else:
        test_list = [test_func() for _ in range(test_samples)]
    for test_sample in test_list:
        test_match = search(test_regex, test_sample)
        test_obj.assertIsInstance(test_match, Match)