# Tests for `mac_common.py`

from unittest import TestCase, main

from mactools.mac_common import (
    fill_hex,
    hex_range,
    prepare_oui
)

from tests.test_common import (
    MAC48,
    MAC64,
    SAMPLE_EUI48,
    SAMPLE_EUI64,
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
        test_48_oui = '6026AA'
        test_64_oui = '0011AA'

        for test_case_48 in [MAC48, SAMPLE_EUI48.mac]:
            result = prepare_oui(test_case_48)
            self.assertEqual(result, test_48_oui)
        
        for test_case_64 in [MAC64, SAMPLE_EUI64.mac]:
            result = prepare_oui(test_case_64)
            self.assertEqual(result, test_64_oui)


if __name__ == '__main__':
    main()