# MacTools MAC Address Class

from enum import Enum
from re import compile, search
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from mactools.oui_cache.oui_core import OUICache, OUIRecord

from functools import cached_property

class Notation(Enum):
    CLEAN = ''
    COLON = ':'
    PERIOD = '.'
    HYPHEN = '-'
    SPACE = ' '

## Universal
HEX_REGEX = r'[a-fA-F0-9]'
MAC_PORTION_REGEX = f'{HEX_REGEX}{{2}}[:\-\. ]?'
EUI48_MAC_REGEX = compile(f'({MAC_PORTION_REGEX}){{6}}')
EUI64_MAC_REGEX = compile(f'({MAC_PORTION_REGEX}){{8}}')

class MacAddress:
    """
    Wrapper and handler for MAC Addresses
    """
    def __init__(self, mac: Union[str, int], format: Notation = Notation.COLON,
                 oui_cache: 'OUICache' = None):
        
        eui = self.validate_mac(mac)
        if not eui:
            raise ValueError(f'{mac} is not a valid MAC Address')
        
        self.__mac = mac
        self.__eui = eui
        self.__oui_record: 'OUIRecord' = None
        self.format = format

        if oui_cache:
            self.__oui_record = oui_cache.get_record(mac)

    def __str__(self):
        format_map = {
            Notation.CLEAN: self.clean,
            Notation.COLON: self.colon,
            Notation.PERIOD: self.period,
            Notation.HYPHEN: self.hyphen,
            Notation.SPACE: self.space,
        }
        return format_map.get(self.format)
    
    def __repr__(self):
        return f'EUI{self.__eui}({str(self)})'

    def __hash__(self) -> int:
        return hash(self.clean)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MacAddress):
            return False
        return self.clean == other.clean

    def __add__(self, value: int):
        """
        Returns the shifted MAC when adding a number
        """
        return self.number_to_hex_mac(self.decimal + value, self.format)

    def __sub__(self, value: Union[int, 'MacAddress']):
        """
        Returns a shifted MAC when `value` is a number or the integer difference
        between two MACs when `value` is another MAC address
        """
        if isinstance(value, MacAddress):
            return self.decimal - value.decimal
        return self.number_to_hex_mac(self.decimal - value, self.format)

    @classmethod
    def validate_mac(cls, mac_input: Union[str, int]) -> int:
        """
        Validates a string and returns `bool` for the results and `int` for the
        EUI if it passes
        """
        if isinstance(mac_input, int):
            mac_input = MacAddress.number_to_hex_mac(mac_input)
        
        mac_candidate = mac_input.strip()

        match_case = {
            EUI64_MAC_REGEX: 64,
            EUI48_MAC_REGEX: 48
        }

        for regex, value in match_case.items():
            mac_match = search(regex, mac_candidate)
            if mac_match:
                return value
            
        return 0

    # PROPERTIES

    @property
    def vendor(self) -> Optional[str]:
        """
        Returns the vendor if the IEEE lookup was made
        """
        if self.__oui_record:
            return self.__oui_record.vendor
        
    @property
    def ieee_record(self) -> Optional['OUIRecord']:
        """
        Returns the `OUIRecord` if it was added
        """
        return self.__oui_record

    @cached_property
    def clean_oui(self) -> str:
        """
        Return a clean OUI
        """
        mac = self.format_mac_address(self.__mac, Notation.CLEAN)
        return mac[0:6]

    @cached_property
    def oui(self) -> str:
        """
        Returns OUI in the MAC's `format`
        """
        mac = self.format_mac_address(self.__mac, self.format)

        # The string length will vary between 6 to 8 depending on delimiters
        slice_pad = {
            Notation.CLEAN: 0,
            Notation.PERIOD: 1,
        }

        return mac[0:6+slice_pad.get(self.format, 2)]
    
    @cached_property
    def binary(self) -> int:
        """
        Return Binary Form
        """
        return self.number_to_binary(self.decimal, self.__eui)

    @cached_property
    def decimal(self) -> int:
        """
        Returns the decimal form
        """
        return self.hex_to_number(self.__mac)
    
    @cached_property
    def clean(self) -> str:
        """
        Returns the clean Form
        """
        return self.clean_mac_address(self.__mac)
    
    @cached_property
    def colon(self) -> str:
        """
        Returns the Colon-separated Form
        """
        return self.format_mac_address(self.__mac, Notation.COLON)
    
    @cached_property
    def period(self) -> str:
        """
        Returns the Period-separated Form
        """
        return self.format_mac_address(self.__mac, Notation.PERIOD)
    
    @cached_property
    def hyphen(self) -> str:
        """
        Returns the Hyphen-separated Form
        """
        return self.format_mac_address(self.__mac, Notation.HYPHEN)
    
    @cached_property
    def space(self) -> str:
        """
        Returns the Space-separated Form
        """
        return self.format_mac_address(self.__mac, Notation.SPACE)
    
    # CONVERSION METHODS

    @classmethod
    def clean_mac_address(cls, input_mac: str, *args, **kwargs):
        """
        Removes delimiters from a MAC Address
        """
        mac = input_mac.strip()
        for char in [':', '.', '-', ' ']:
            mac = mac.replace(char, '')
        return mac

    @classmethod
    def format_mac_address(cls, mac_address: str,
                           delimiter: Notation = Notation.COLON, 
                           case: str = 'upper',
                           *args, **kwargs):
        """
        Takes a MAC address and re-formats it appropriately
        """
        mac_address = cls.clean_mac_address(mac_address)

        delimiter: str = delimiter.value

        slice_len = 4 if delimiter == '.' else 2
        mac_slices = [mac_address[i:i+slice_len] for i in range(0, len(mac_address), slice_len)]
        joined_mac = delimiter.join(mac_slices)

        case_dict = {
            'upper': joined_mac.upper,
            'lower': joined_mac.lower
        }

        case = case.lower().strip()
        case_result = case_dict.get(case, joined_mac.upper)

        return case_result()
    
    @classmethod
    def hex_to_number(cls, input_mac: str, *args, **kwargs) -> int:
        """
        Returns a numerical representation of a MAC Address from hex
        """
        return int(cls.clean_mac_address(input_mac), 16)
    
    @classmethod
    def number_to_hex_mac(cls, input_number: int,
                          form: Notation = Notation.COLON,
                          bit_length: int = 48,
                          *args, **kwargs) -> str:
        """
        Returns a hexadecimal representation for a MAC Address from a number
        """
        clean_hex = hex(input_number)[2:]
        fill_required = int(len(clean_hex) - (bit_length / 4))
        leading_zeros = ''.zfill(fill_required)
        filled_hex = f'{leading_zeros}{clean_hex}'
        return cls.format_mac_address(filled_hex, form)

    @classmethod
    def number_to_binary(cls, input_number: int, bit_length: int) -> int:
        """
        Return a binary representation of the input
        """
        return int(bin(input_number)[2:].zfill(bit_length))
