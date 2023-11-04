# OUI tests

from unittest import TestCase, main
from unittest.mock import Mock, patch
from os import path, remove

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import _patch_default_new

from tests.test_common import (
    OUICache,
    OUI_CORE_PATH,
    OUI_CLASSES_PATH,
    TEST_OUI_STRING,
    TEST_RECORD,
    TEST_CACHE,
)

from mactools.oui_cache.oui_core import (
    get_oui_cache,
    get_oui_record,
    get_oui_vendor,
)

from mactools.oui_cache.oui_common import PICKLE_DIR

# Fixed Test Data
TEST_RESPONSE_TEXT = '''
60-26-AA   (hex)		Cisco Systems, Inc
6026AA     (base 16)		Cisco Systems, Inc
				80 West Tasman Drive
				San Jose  CA  94568
				US
'''

class TestOUICacheAPI(TestCase):
    """
    Test class to ensure API call and cache construction
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.patchers: list[_patch_default_new] = []
        cls.mock_response = Mock()
        cls.mock_response.status_code = 200
        cls.mock_response.text = TEST_RESPONSE_TEXT

        cls.write_test_path = PICKLE_DIR.replace('oui.pkl', 'test-oui.pkl')

        oui_text_patch = patch(f'{OUI_CORE_PATH}.get_oui_text', return_value=cls.mock_response)
        cls.patchers.append(oui_text_patch)

        cls.patchers.append(patch('builtins.print', return_value=None))

        for oui_path in [OUI_CLASSES_PATH, OUI_CORE_PATH]:
            cls.patchers.append(patch(f'{oui_path}.VERSION', 'TEST'))
            cls.patchers.append(patch(f'{oui_path}.PICKLE_DIR', cls.write_test_path))

        for patcher in cls.patchers:
            patcher.start()
    
    @classmethod
    def tearDownClass(cls) -> None:
        for patcher in cls.patchers:
            patcher.stop()
    
    def setUp(self) -> None:
        # Reset any changes to the Mock
        self.mock_response.status_code = 200

    def test_get_new_cache(self):
        """
        Test creation of the test cache
        """
        local_cache = get_oui_cache(rebuild=True)
        self.assertIsInstance(local_cache, OUICache)
        self.assertEqual(local_cache.get_record(TEST_OUI_STRING), TEST_RECORD)
        self.assertEqual(local_cache.get_vendor(TEST_OUI_STRING), TEST_RECORD.vendor)

    def test_get_cache_exceptions(self):
        """
        Test exception cases of `get_oui_cache`
        """
        local_cache = get_oui_cache(rebuild=False)
        delattr(local_cache, 'cache_version')
        local_cache.write_oui_cache()

        new_cache = get_oui_cache(rebuild=False)
        self.assertEqual(new_cache.cache_version, 'TEST')
         

    def test_get_cache_404(self):
        """
        Test for failure to get a local cache with a bad HTTP status code
        """
        self.mock_response.status_code = 404
        local_cache = get_oui_cache(rebuild=True)
        self.assertEqual(local_cache, None)

    def test_write_cache(self):
        """
        Test for writing an `OUICache` the user's cache file
        """
        local_cache = OUICache({TEST_OUI_STRING.upper(): TEST_RECORD})
        local_cache.cache_version = 'TEST'
        local_cache.write_oui_cache()

        new_oui_cache = get_oui_cache()
        self.assertEqual(new_oui_cache.cache_version, 'TEST')

        if path.exists(self.write_test_path):
            remove(self.write_test_path)
            

class TestOUICacheRecords(TestCase):
    """
    Test class to check record fetching from a supplied test cache
    """
    @classmethod
    def setUpClass(cls):
        cls.cache_patcher = patch(f'{OUI_CORE_PATH}.get_oui_cache', return_value=TEST_CACHE)
        cls.mock_get_oui_cache = cls.cache_patcher.start()
        cls.TEST_LIST = [TEST_OUI_STRING for _ in range(3)]
        
    @classmethod
    def tearDownClass(cls):
        cls.cache_patcher.stop()

    def test_get_record(self):
        """
        Standard test of fetching a single record
        """
        test_get = get_oui_record(TEST_OUI_STRING)
        self.assertEqual(test_get, TEST_RECORD)

        # Unique case for getting specified/reserved MAC records
        test_get_fixed = get_oui_record('3333EA')
        self.assertEqual(test_get_fixed.vendor, 'IPv6 Multicast')

    def test_get_vendor(self):
        """
        Standard test of fetching a single vendor string
        """
        test_get = get_oui_vendor(TEST_OUI_STRING)
        self.assertEqual(test_get, TEST_RECORD.vendor)

    def test_get_record_list(self):
        """
        Standard test of fetching a list of records
        """
        test_get = get_oui_record(self.TEST_LIST)
        for record in test_get:
            self.assertEqual(record, TEST_RECORD)

    def test_invalid_get_oui_item(self):
        """
        Tests for the inner functionality of cache getting
        """
        with self.assertRaises(ValueError):
            get_oui_record([10])
        with self.assertRaises(ValueError):
            get_oui_record(10)

if __name__ == '__main__':
    main()