# MAC Address Tests

# Python Modules
from re import match, Pattern
from typing import Optional
from unittest import TestCase, main

# Local Modules
from tests.test_common import (
    TestMac,
    SAMPLE_EUI48,
    SAMPLE_EUI64,
    TEST_RECORD,
    TEST_CACHE
)

from mactools import (
    MacAddress,
    MacNotation,
    create_random_hex_string,
    create_random_mac,
)

from mactools.basemac import (
    HEX_PATTERN,
    MAC_PORTION,
    EUI48_REGEX,
    EUI64_REGEX,
)


class TestFunctions(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mac48 = MacAddress(SAMPLE_EUI48.mac)
        cls.mac64 = MacAddress(SAMPLE_EUI64.mac)

        cls.mac_lookup: dict[MacAddress, TestMac] = {
            cls.mac48: SAMPLE_EUI48,
            cls.mac64: SAMPLE_EUI64
        }

    def test_regex(self):
        fixed_lookup: dict[Pattern[str], str] = {
            EUI48_REGEX: SAMPLE_EUI48.mac,
            EUI64_REGEX: SAMPLE_EUI64.mac
        }

        random_lookup: dict[Pattern[str], str] = {
            HEX_PATTERN: f'{create_random_hex_string()}',
            MAC_PORTION: f'{create_random_hex_string()}:',
            EUI48_REGEX: create_random_mac(),
            EUI64_REGEX: create_random_mac(64),
        }

        for case_lookup in [fixed_lookup, random_lookup]:
            for regex, case in case_lookup.items():
                self.assertTrue(match(regex, case))

    def test_mac_validation(self):
        for invalid_mac in [
            'a',
            '00:11:AA:BB',
            '00:11:AA:BB:99',
            '0011AABB99',
            '00-1-2-3-4'
        ]:
            try:
                MacAddress(invalid_mac)
            except ValueError as e:
                self.assertIsInstance(e, ValueError)

        valid_macs: list[str] = [SAMPLE_EUI48.decimal]
        for eui in [48, 64]:
            for mac_MacNotation in MacNotation:
                valid_macs.append(create_random_mac(eui, mac_MacNotation))

        for valid_mac in valid_macs:
            self.assertIsInstance(MacAddress(valid_mac), MacAddress)

    def test_cache_with_creation(self):
        """
        Tests passing `OUICache` instance on creation and auto-fetching record
        """
        local_test_mac = MacAddress(SAMPLE_EUI48.mac, cache=TEST_CACHE)
        self.assertEqual(local_test_mac.vendor, TEST_RECORD.get('vendor'))

    def test_mac_get_vendor(self):
        """
        Tests 
        """
        local_test_mac = MacAddress(SAMPLE_EUI48.mac, cache=TEST_CACHE)
        self.assertEqual(local_test_mac.vendor, TEST_CACHE.get_vendor(SAMPLE_EUI48.mac))


    """
    Test the various MAC Properties
    """
    def mac_test_iterator(self, mac_attr: str, tested_attr: str,
                          replacements: Optional[tuple[str]] = None,
                          slicing: Optional[tuple[int]] = None):
        """
        De-duplication function for testing MAC forms for 48 and 64-bit versions
        """
        for mac, test_mac in self.mac_lookup.items():
            mac_detail: str = getattr(mac, mac_attr)
            match_detail: str = getattr(test_mac, tested_attr)

            if replacements:
                match_detail = match_detail.replace(*replacements)

            if slicing:
                start, stop = slicing
                match_detail = match_detail[start:stop]

            self.assertEqual(mac_detail, match_detail)

    def test_mac_oui(self):
        self.mac_test_iterator('oui', 'mac', slicing=(0, 8))

    def test_mac_clean_oui(self):
        self.mac_test_iterator('clean_oui', 'mac', (':', ''), (0, 6))

    def test_mac_clean(self):
        self.mac_test_iterator('clean', 'mac', (':', ''))

    def test_mac_colon(self):
        self.mac_test_iterator('colon', 'mac')

    def test_mac_period(self):
        self.assertEqual(self.mac48.period, '246D.5EBB.99CC')
        self.assertEqual(self.mac64.period, '246D.5E00.00BB.99DD')

    def test_mac_hyphen(self):
        self.mac_test_iterator('hyphen', 'mac', (':', '-'))

    def test_mac_space(self):
        self.mac_test_iterator('space', 'mac', (':', ' '))

    def test_mac_decimal(self):
        self.mac_test_iterator('decimal', 'decimal')

    def test_mac_binary(self):
        self.mac_test_iterator('binary', 'binary')

    """
    Test Magic Methods
    """
    def test_magic_str(self):
        for mac, test_mac in self.mac_lookup.items():
            self.assertEqual(str(mac), test_mac.mac)

    def test_magic_hash(self):
        for mac, test_mac in self.mac_lookup.items():
            self.assertEqual(mac.__hash__(), hash(test_mac.mac.replace(':','')))

    def test_magic_equal(self):
        for mac, test_mac in self.mac_lookup.items():
            self.assertEqual(mac, MacAddress(test_mac.mac))
            self.assertFalse('this should be false' == mac)

    def test_magic_add(self):
        self.assertEqual(self.mac48+1, '24:6D:5E:BB:99:CD')
        self.assertEqual(self.mac64+1, '24:6D:5E:00:00:BB:99:DE')
        
        self

    def test_magic_subtract(self):
        # Testing MAC-and-MAC subtraction
        for mac in self.mac_lookup:
            self.assertEqual(mac-mac, 0)
        # Testing MAC-and-number subtraction
        self.assertEqual(self.mac48-1, '24:6D:5E:BB:99:CB')
        self.assertEqual(self.mac64-1, '24:6D:5E:00:00:BB:99:DC')


if __name__ == '__main__':
    main()
    # oui_cache_patch.stop()