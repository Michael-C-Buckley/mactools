# MacTools API tests

# Python Modules
from json import dumps
from unittest import TestCase, main
from unittest.mock import Mock, patch

# Local Modules

from mactools.oui_cache.oui_api_calls import (
    httpx_get,
    get_oui_csv,
    mac_lookup_call,
    vendor_oui_lookup,
)

from tests.test_oui_cache import MAL_RESPONSE_TEXT
from tests.test_common import (
    TEST_RECORD,
    MAC48,
    SAMPLE_EUI48
)


API_DIR = 'mactools.oui_cache.oui_api_calls'

class APITests(TestCase):
    """
    Simple tests to cover the simple API calls needed
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_mac = MAC48
        cls.test_mac_str = SAMPLE_EUI48.mac
        cls.test_oui = TEST_RECORD.get('oui')
        cls.test_vendor = TEST_RECORD.get('vendor')

    def prepare_mock(func: callable, *args) -> callable:
        """
        Decorator to yield a new, local `Mock` for HTTP responses
        """
        def wrapper(self, *args):
            mock_response: Mock = Mock()
            mock_response.status_code = 200
            mock_response.text = dumps(TEST_RECORD)
            return func(self, mock_response, *args)
        return wrapper
    
    def multi_test_cases(self, func: callable, expected_result, *args) -> None:
        """
        Test factory for conducting multiple tests of a function
        """
        for test_input in [self.test_mac, self.test_mac_str]:
            result = func(test_input)
            self.assertEqual(result, expected_result)
    
    @prepare_mock
    def test_httpx_get(self, mock_response: Mock):
        """
        Tests for valid and error cases
        """
        with patch(f'{API_DIR}.get', return_value=mock_response):
            test_response = httpx_get('https://www.google.com')
            self.assertTrue(test_response, mock_response)

        with patch(f'{API_DIR}.get', side_effect=ValueError('Test Error')):
            mock_response.status_code = 404
            with self.assertRaises(Exception):
                test_response = httpx_get('https://www.google.com')
    
    # ADD CSV TESTS
    @prepare_mock
    def test_get_oui_text(self, mock_response: Mock):
        with patch(f'{API_DIR}.httpx_get', return_value=mock_response):
            mock_response.text = MAL_RESPONSE_TEXT
            test_response = get_oui_csv()
            self.assertEqual(test_response, mock_response)

    @prepare_mock
    def test_mac_lookup_call(self, mock_response: Mock):
        with patch(f'{API_DIR}.httpx_get', return_value=mock_response):
            self.multi_test_cases(mac_lookup_call, TEST_RECORD)

    @prepare_mock
    def test_vendor_oui_lookup(self, mock_response: Mock):
        mock_response = self.test_vendor
        with patch(f'{API_DIR}.httpx_get', return_value=mock_response):
            self.multi_test_cases(vendor_oui_lookup, self.test_vendor)


if __name__ == '__main__':
    main()