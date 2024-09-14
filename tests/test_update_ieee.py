# MacTools IEEE Updater Tests

# Python Modules
from os import path
from importlib.resources import files
from unittest import TestCase, main
from unittest.mock import MagicMock, Mock, patch, mock_open

from time import sleep

# Local Modules
from mactools.update_ieee import update_ieee_files

class TestUpdate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_base_url = 'https://standards-oui.ieee.org/'
        cls.base_dest_path = files('mactools').joinpath('resources/ieee')
        cls.endpoints = ['oui/oui', 'oui28/mam', 'oui36/oui36']
    
        cls.print_patch = patch('builtins.print', return_value=None)
        cls.print_patch.start()

        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.print_patch.stop()
    
    @patch('mactools.update_ieee.open', new_callable=mock_open)
    @patch('mactools.update_ieee.urlopen')
    def test_update_files(self, mock_urlopen: Mock, mock_fileopen: Mock):
        """
        Tests the successful update
        """

        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.read.return_value = mock_response

        test_result = update_ieee_files()

        self.assertEqual(test_result, True)
        self.assertEqual(mock_urlopen.call_count, 3)

        for i, endpoint in enumerate(self.endpoints):
            args, kwargs = mock_urlopen.call_args_list[i]
            url = f'{self.test_base_url}{endpoint}.csv'
            self.assertEqual(args[0].full_url, url)

    @patch('mactools.update_ieee.urlopen')
    def test_update_failures(self, mock_retrieve: Mock):
        mock_retrieve.side_effect = Exception('Mock Exception')
        test_result = update_ieee_files()
        self.assertEqual(test_result, False)

    @patch('mactools.update_ieee.path')
    def test_skip_updating_file(self, mock_path: Mock):
        mock_path.return_value = True
        test_result = update_ieee_files(overwrite=False)
        self.assertEqual(test_result, True)
    

if __name__ == '__main__':
    main()