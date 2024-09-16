# MacTools OUI tests

# Python Modules
from unittest import TestCase, main
from unittest.mock import Mock, patch, DEFAULT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import _patch_default_new

# Local modules
from mactools.oui_cache.oui_core import (
    get_oui_cache, get_oui_record, get_oui_vendor,
)
from tests.test_common import (
    OUICache, generate_random_str, URL_MOCK, OUI_COMMON_PATH,
    TEST_OUI_STRING, TEST_VENDOR, TEST_OUI_DICT
)

class TestOUICache(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.patchers: list[_patch_default_new] = []

        cls.patchers.append(patch('builtins.print', return_value=None))
        cls.patchers.append(patch('urllib.request.urlopen', return_value=URL_MOCK))

        for patcher in cls.patchers:
            patcher.start()

        cls.cache = get_oui_cache()
        cls.cache.attempt_update = False
    
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

    @patch(f'os.path.exists')
    @patch.multiple(OUI_COMMON_PATH, update_ieee_files=DEFAULT, process_ieee_csv=DEFAULT)
    def test_cache_with_updates(self, path_exists: Mock, update_ieee_files: Mock, process_ieee_csv: Mock):
        path_exists.return_value = False
        update_ieee_files.return_value = True
        process_ieee_csv.side_effect = Exception('Test Interrupt')
        
        with self.assertRaises(Exception):
            get_oui_cache(regenerate=True)
            update_ieee_files.assert_called_once()

    def test_get_vendor(self):
        """
        Standard test of fetching a single vendor string
        """
        for test_case in TEST_VENDOR:
            test_get = get_oui_vendor(TEST_OUI_STRING[test_case])
            self.assertEqual(test_get, TEST_VENDOR[test_case])

    def test_get_record(self):
        """
        Standard testing of fetching a record
        """
        for test_case in TEST_VENDOR:

            expected = {
                'oui': TEST_OUI_STRING[test_case],
                'vendor': TEST_VENDOR[test_case],
                'address': 'ADDRESS INFO',
                'error': False,
            }

            test_get = get_oui_record(TEST_OUI_STRING[test_case])
            self.assertEqual(test_get, expected)

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
            get_oui_vendor(10)

    def test_invalid_oui_cases(self):
        """
        Test the record fetching for cases where the input mac is invalid
        """
        local_cache = get_oui_cache()
        test_cases = {
            'asdfasdf': 'This is not a valid hex string',
            'AAAA': 'OUI/MAC is shorter than 6 hex characters (24 bits) and too short to be any OUI',
            'AAAA00001111DDDD2222FFFF': 'OUI/MAC is longer than 16 hex characters (64 bits) and longer than MAC addresses can be'
        }

        for test_case, result_note in test_cases.items():
            result = local_cache.get_record(test_case)
            expected = {'input': test_case, 'error': True, 'note': result_note}
            self.assertEqual(result, expected)

    def test_fuzz_oui_cache(self):
        with patch('mactools.oui_cache.oui_classes.create_oui_dict') as patched_update:
            patched_update.return_value = TEST_OUI_DICT
            for i in range(100000):
                test_str = generate_random_str()
                test_result = get_oui_record(test_str)


if __name__ == '__main__':
    main()