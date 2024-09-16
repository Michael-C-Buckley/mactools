# Common Test Library

# Python Modules
from dataclasses import dataclass
from json import dumps
from random import choice, randint
from re import search, compile, Match
from string import ascii_letters, digits, punctuation
from typing import Any
from unittest import TestCase
from unittest.mock import Mock, patch

# STOP THE API COOLDOWN
patch('mactools.oui_cache.oui_classes.sleep', return_value=None).start()

# Local Modules
from mactools import MacAddress
from mactools.oui_cache.oui_classes import OUICache, OUIType

# Fake MACs for internal testing
TEST_OUI_STRING = {
    OUIType.OUI: '246D5E',
    OUIType.OUI28: '79B74DA',
    OUIType.OUI36: '24B7BD603',
}
TEST_VENDOR = {
    OUIType.OUI: 'TEST Systems, Inc',
    OUIType.OUI28: 'TEST Labs',
    OUIType.OUI36: 'Micro TEST Inc',
}

TEST_RECORD = {
    'oui': TEST_OUI_STRING[OUIType.OUI],
    'vendor': TEST_VENDOR[OUIType.OUI],
    'address': 'ADDRESS INFO'
}
TEST_OUI_DICT = {i: {TEST_OUI_STRING[i]: {'vendor': TEST_VENDOR[i], 'oui': TEST_OUI_STRING[i], 'address': 'ADDRESS INFO'}} for i in TEST_VENDOR}
TEST_CACHE = OUICache(TEST_OUI_DICT, False)

OUI_CORE_PATH = 'mactools.oui_cache.oui_core'
OUI_COMMON_PATH = 'mactools.oui_cache.oui_common'
OUI_CLASSES_PATH = 'mactools.oui_cache.oui_classes'

# urllib mock
URL_MOCK = Mock()
URL_MOCK.status = 200
URL_MOCK.read.return_value = b'{"success":true,"found":true,"macPrefix":"AA0000","company":"Test GET"}'

@dataclass
class TestMac:
    mac: str
    binary: int
    decimal: int


# Fixed, Reusable Test Cases
SAMPLE_EUI48 = TestMac('24:6D:5E:BB:99:CC',
    1001000110110101011110101110111001100111001100,
    40052159388108)

SAMPLE_EUI64 = TestMac('24:6D:5E:00:00:BB:99:DD',
    10010001101101010111100000000000000000101110111001100111011101,
    2624857511932172765)

MAC48 = MacAddress(SAMPLE_EUI48.mac)
MAC64 = MacAddress(SAMPLE_EUI64.mac)

def prepare_mock(status_code: int = 200):
    """
    Decorator to yield a new, local `Mock` for HTTP responses
    """
    def inner_decorator(func: callable, *args) -> callable:
        def wrapper(self, *args):
            mock_response: Mock = Mock()
            mock_response.status_code = status_code
            mock_response.text = dumps(TEST_RECORD)
            return func(self, mock_response, *args)
        return wrapper
    return inner_decorator

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

def generate_random_str(length: int = 0) -> str:
    """
    Generate a random string of characters, digits, and punctuation for fuzzing
    """
    length = randint(0,50) if length == 0 else length
    chars = ascii_letters + digits + punctuation
    return ''.join(choice(chars) for _ in range(length))
