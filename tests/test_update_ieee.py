# MacTools IEEE Updater Tests

# Python Modules
from os import path
from pkg_resources import resource_filename
from unittest import TestCase, main
from unittest.mock import Mock, patch

# Local Modules
from mactools.update_ieee import update_ieee_files

class TestUpdate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_base_url = 'https://standards-oui.ieee.org/'
        cls.base_dest_path = resource_filename('mactools', 'resources/ieee')
        cls.endpoints = ['oui/oui', 'oui28/mam', 'oui36/oui36']
    
        cls.print_patch = patch('builtins.print', return_value=None)
        cls.print_patch.start()

        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.print_patch.stop()
    
    @patch('mactools.update_ieee.urlretrieve')
    def test_update_files(self, mock_retrieve: Mock):
        """
        Tests the successful update
        """
        test_result = update_ieee_files()

        self.assertEqual(test_result, True)
        self.assertEqual(mock_retrieve.call_count, 3)

        for i, endpoint in enumerate(self.endpoints):
            args, kwargs = mock_retrieve.call_args_list[i]
            dest_path = f'{path.join(self.base_dest_path, endpoint.split("/")[1])}.csv'
            url = f'{self.test_base_url}{endpoint}.csv'
            self.assertEqual(args[0], url)
            self.assertEqual(args[1], dest_path)

    @patch('mactools.update_ieee.urlretrieve')
    def test_update_failures(self, mock_retrieve: Mock):
        mock_retrieve.side_effect = Exception('Mock Exception')
        test_result = update_ieee_files()
        self.assertEqual(test_result, False)

if __name__ == '__main__':
    main()