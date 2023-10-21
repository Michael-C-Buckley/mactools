from mactools.oui_cache.oui_api_calls import (
    httpx_get,
    get_oui_text
)

from unittest import TestCase, main
from unittest.mock import Mock, patch

API_DIR = 'mactools.oui_cache.oui_api_calls'

class APITests(TestCase):
    """
    Simple tests to cover the simple API calls needed
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_response = Mock()
    
    def test_httpx_get(self):
        """
        Tests for valid and error cases
        """
        with patch(f'{API_DIR}.get', return_value=self.mock_response):
            self.mock_response.status_code = 200
            test_response = httpx_get('https://www.google.com')
            self.assertTrue(test_response, self.mock_response)

        with patch(f'{API_DIR}.get', side_effect=ValueError('Test Error')):
            self.mock_response.status_code = 404
            with self.assertRaises(Exception):
                test_response = httpx_get('https://www.google.com')
    
    def test_get_oui_text(self):
        with patch(f'{API_DIR}.httpx_get', return_value=self.mock_response):
            test_response = get_oui_text()
            self.assertEqual(test_response, self.mock_response)


if __name__ == '__main__':
    main()