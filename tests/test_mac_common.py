# Tests for `mac_common.py`

# Python Modules
from unittest import TestCase, main

# Local Modules
from mactools.tools_common import MAC_PATTERN

from mactools import (
    fill_hex,
    hex_range,
    prepare_oui,
    create_random_hex_bit,
    create_random_hex_string,
    create_random_mac,
)

from tests.test_common import (
    MAC48,
    MAC64,
    SAMPLE_EUI48,
    SAMPLE_EUI64,
    test_regex_comparison,
)

class TestMACCommon(TestCase):
    
    def test_fill_hex(self):
        """
        Tests for the various cases of `fill_hex`
        """
        test_case_dict = {
            111: '006F',
            'ac': '00AC'
        }
        for test_input, result in test_case_dict.items():
            self.assertEqual(fill_hex(test_input, 4), result)

    def test_hex_range(self):
        """
        Tests for the various cases of `hex_range`
        """
        expected_result_list = []

        for i in range(256):
            test_result = hex(i)[2:].upper()
            if len(test_result) == 1:
                test_result = f'0{test_result}'
            expected_result_list.append(test_result)

        for i, test_mac in enumerate(hex_range(2)):
            self.assertEqual(expected_result_list[i], test_mac)

    def test_prepare_oui(self):
        """
        Tests for the various cases of `prepare_oui`
        """
        # This OUI is from the pre-defined sample MACs used in testing
        test_oui = '246D5E'

        for test_case_48 in [MAC48, SAMPLE_EUI48.mac]:
            result = prepare_oui(test_case_48, False)
            self.assertEqual(result, test_oui)
        
        for test_case_64 in [MAC64, SAMPLE_EUI64.mac]:
            result = prepare_oui(test_case_64, False)
            self.assertEqual(result, test_oui)

    def test_create_random_hex_bit(self):
        """
        Test for creating hex bits
        """
        test_regex_comparison(self, r'[A-F\d]', create_random_hex_bit, 1600)

    def test_create_random_hex_string(self):
        """
        Test for creating hex strings
        """
        local_kwargs = {
            'test_obj': self,
            'test_func': create_random_hex_string,
            'test_samples': 100,
        }
        for test_case in range(1, 10):
            local_kwargs['pattern'] = r'[A-F\d]{' + str(test_case) + '}'
            local_kwargs['test_arg'] = test_case
            test_regex_comparison(**local_kwargs)

    def test_create_random_mac(self):
        """
        Test for creating MAC addresses
        """
        local_kwargs = {
            'test_obj': self,
            'test_func': create_random_mac,
            'test_samples': 100,
            'pattern': MAC_PATTERN,
        }
        for eui in [48, 64]:
            test_regex_comparison(**local_kwargs, test_arg=eui)

        with self.assertRaises(ValueError):
            create_random_mac(eui=999)


if __name__ == '__main__':
    main()