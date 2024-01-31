# MacTools CLI Tests

# Python Modules
from re import search
from sys import executable
from subprocess import run
from unittest import TestCase, main
from unittest.mock import patch

# Local Modules
from tests.test_common import TEST_CACHE,TEST_OUI_STRING, TEST_VENDOR
from mactools.cli.oui import main as oui_cli_main, handle_args

CLI_OUI_DIR = 'mactools.cli.oui'

class CLITest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.print_patch = patch('builtins.print', return_value=None)
        cls.print_patch.start()
        cls.cache_patch = patch(f'{CLI_OUI_DIR}.get_oui_cache', return_value=TEST_CACHE)
        cls.cache_patch.start()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.print_patch.stop()
        cls.cache_patch.stop()
        return super().tearDownClass()
    
    @patch(f'{CLI_OUI_DIR}.main')
    @patch('sys.argv', ['oui', 'test_oui'])
    def test_handle_args(self, mock_main):
        handle_args()
        mock_main.assert_called_once_with('test_oui')
    
    def test_oui_cli_main(self):
        """
        Test for the output function of the CLI
        """
        for oui_type in TEST_OUI_STRING:
            vendor = oui_cli_main(TEST_OUI_STRING[oui_type])
            output_match = search(TEST_VENDOR[oui_type], vendor)
            self.assertTrue(output_match)

        no_match = oui_cli_main('6026aa')
        self.assertIsNone(no_match)

        error = oui_cli_main(101)
        self.assertEqual(error, ValueError)

    def test_oui_cli_process(self):
        """
        Integration test using `subprocess` library since patching does not work.
        This uses a real OUI off the real cache.
        """
        cli_path = 'mactools/cli/oui.py'
        cli_list = [executable, cli_path, '6026aa']
        result = run(cli_list, capture_output=True, text=True)
        result_match = search(r'Cisco', result.stdout)
        self.assertTrue(result_match)
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    main()