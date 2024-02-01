# MacTools OUI tests

# Python Modules
from unittest import TestCase, main
from unittest.mock import patch
from re import search
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import _patch_default_new

# Local modules
from mactools.oui_cache.oui_core import (
    get_oui_cache,
    get_oui_vendor,
)
from tests.test_common import (
    OUICache,
    TEST_OUI_STRING,
    TEST_VENDOR,
)

class TestOUICache(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.patchers: list[_patch_default_new] = []

        cls.patchers.append(patch('builtins.print', return_value=None))

        for patcher in cls.patchers:
            patcher.start()
    
    @classmethod
    def tearDownClass(cls) -> None:
        for patcher in cls.patchers:
            patcher.stop()
    
    def test_get_new_cache(self):
        """
        Test creation of the test cache
        """
        local_cache = get_oui_cache()
        self.assertIsInstance(local_cache, OUICache)
        for test_case in TEST_OUI_STRING:
            self.assertEqual(local_cache.get_vendor(TEST_OUI_STRING[test_case]), TEST_VENDOR[test_case])
        
        second_cache = get_oui_cache()
        self.assertEqual(local_cache, second_cache)

    def test_get_vendor(self):
        """
        Standard test of fetching a single vendor string
        """
        for test_case in TEST_VENDOR:
            test_get = get_oui_vendor(TEST_OUI_STRING[test_case])
            self.assertEqual(test_get, TEST_VENDOR[test_case])

    def test_get_vendor_list(self):
        """
        Fetching the records of a list of items
        """
        test_list = [v for v in TEST_OUI_STRING.values()]
        result_list = get_oui_vendor(test_list)

        for result, test_case in zip(result_list, TEST_VENDOR.values()):
            self.assertEqual(result, test_case)


    def test_locally_administered(self):
        test_result = get_oui_vendor('4EAAAA')
        self.assertEqual(test_result, 'Locally administered')

    def test_fixed_specific(self):
        test_result = get_oui_vendor('FF:FF:FF:FF:FF:FF')
        self.assertEqual(test_result, 'Broadcast')

    def test_mac_range(self):
        test_result = get_oui_vendor('33:33:0A')
        self.assertEqual(test_result, 'IPv6 Multicast')

    def test_invalid_get_oui_item(self):
        """
        Tests for the inner functionality of cache getting
        """
        with self.assertRaises(ValueError):
            get_oui_vendor([10])
        with self.assertRaises(ValueError):
            get_oui_vendor(10)

if __name__ == '__main__':
    main()