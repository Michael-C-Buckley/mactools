# MacTools Base MAC Address Class

# Python Modules
from __future__ import annotations
from enum import Enum
from functools import cached_property
from ipaddress import IPv6Address as IPv6, AddressValueError
from typing import Dict, Optional, Union, TYPE_CHECKING

# Local Modules
from mactools.tools_common import get_hex_value

if TYPE_CHECKING:
    from mactools.oui_cache.oui_core import OUICache

class MacNotation(Enum):
    CLEAN = ''
    COLON = ':'
    PERIOD = '.'
    HYPHEN = '-'
    SPACE = ' '

class BaseMac:
    """
    Wrapper and handler for MAC Addresses
    """
    def __init__(self, mac: Union[str, int], format: MacNotation = MacNotation.COLON,
                 oui_cache: 'OUICache' = None, *args, **kwargs):
        
        eui = self.validate_mac(mac)
        if not eui:
            raise ValueError(f'{mac} is not a valid MAC Address')
        
        self.__mac = mac
        self.__eui = eui
        self.__oui_record: Dict[str, str] = None
        self.format = format

        if oui_cache:
            self.__oui_record = oui_cache.get_record(self.clean_oui)

    def __str__(self):
        format_map = {
            MacNotation.CLEAN: self.clean,
            MacNotation.COLON: self.colon,
            MacNotation.PERIOD: self.period,
            MacNotation.HYPHEN: self.hyphen,
            MacNotation.SPACE: self.space,
        }
        return format_map.get(self.format)
    
    def __repr__(self):
        return f'EUI{self.__eui}({str(self)})'

    def __hash__(self) -> int:
        return hash(self.clean)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseMac):
            return False
        return self.clean == other.clean

    def __add__(self, value: int):
        """
        Returns the shifted MAC when adding a number
        """
        return self.number_to_hex_mac(self.decimal + value, self.format, self.__eui)

    def __sub__(self, value: Union[int, 'BaseMac']):
        """
        Returns a shifted MAC when `value` is a number or the integer difference
        between two MACs when `value` is another MAC address
        """
        if isinstance(value, BaseMac):
            return self.decimal - value.decimal
        return self.number_to_hex_mac(self.decimal - value, self.format, self.__eui)

    @classmethod
    def validate_mac(cls, mac_input: Union[str, int]) -> int:
        """
        Validates a string and returns the EUI value for valid matches or 0 for invalid
        """
        if isinstance(mac_input, int):
            mac_input = BaseMac.number_to_hex_mac(mac_input)

        hex_value = get_hex_value(mac_input)
        return hex_value if hex_value in [48, 64] else 0

    # PROPERTIES

    @property
    def vendor(self) -> Optional[str]:
        """
        Returns the vendor if the IEEE lookup was made
        """
        if self.__oui_record:
            return self.__oui_record.get('vendor')
        
    @cached_property
    def clean_oui(self) -> str:
        """
        Return a clean OUI
        """
        mac = self.format_mac_address(self.__mac, MacNotation.CLEAN)
        return mac[0:6]

    @cached_property
    def oui(self) -> str:
        """
        Returns OUI in the MAC's `format`
        """
        mac = self.format_mac_address(self.__mac, self.format)

        # The string length will vary between 6 to 8 depending on delimiters
        slice_pad = {
            MacNotation.CLEAN: 0,
            MacNotation.PERIOD: 1,
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
        return self.format_mac_address(self.__mac, MacNotation.COLON)
    
    @cached_property
    def period(self) -> str:
        """
        Returns the Period-separated Form
        """
        return self.format_mac_address(self.__mac, MacNotation.PERIOD)
    
    @cached_property
    def hyphen(self) -> str:
        """
        Returns the Hyphen-separated Form
        """
        return self.format_mac_address(self.__mac, MacNotation.HYPHEN)
    
    @cached_property
    def space(self) -> str:
        """
        Returns the Space-separated Form
        """
        return self.format_mac_address(self.__mac, MacNotation.SPACE)
    
    @cached_property
    def eui64_suffix(self) -> str:
        """
        Returns the EUI-64 suffix for an IPv6 address
        """
        if self.__eui == 48:
            eui = str(self.clean)
            swapped = hex(int(eui[1:2], 16)+2)[2:]
            eui = f'{eui[:1]}{swapped}{eui[2:6]}fffe{eui[6:]}'
        else:
            # EUI-64 will assume it doesn't need to be flipped
            eui = self.clean
        return self.format_mac_address(eui, MacNotation.COLON, 'lower', interval=4)
    
    @cached_property
    def link_local_address(self) -> str:
        """
        Returns the IPv6 link-local address based on the MAC address
        """
        return f'fe80::{self.eui64_suffix}'


    # CONVERSION METHODS

    @classmethod
    def clean_mac_address(cls, input_mac: str, *args, **kwargs):
        """
        Removes delimiters from a MAC Address
        """
        if isinstance(input_mac, int):
            mac = cls.number_to_hex_mac(input_mac, MacNotation.CLEAN)
        elif isinstance(input_mac, str):
            mac = input_mac.strip()
            for char in [':', '.', '-', ' ']:
                mac = mac.replace(char, '').upper()
        return mac

    @classmethod
    def format_mac_address(cls, mac_address: str,
                           delimiter: MacNotation = MacNotation.COLON, 
                           case: str = 'upper', interval: int = None,
                           *args, **kwargs) -> str:
        """
        Takes a MAC address and re-formats it appropriately
        """
        mac_address = cls.clean_mac_address(mac_address)

        delimiter: str = delimiter.value

        if interval is None:
            slice_len = 4 if delimiter == '.' else 2
        else:
            slice_len = interval
        
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
                          form: MacNotation = MacNotation.COLON,
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
    
    def get_global_address(self, global_prefix: str) -> IPv6:
        """
        Returns the GUA for the MAC address with supplied prefix
        """
        ip_address = f'{global_prefix}:{self.eui64_suffix}'
        try:
            return IPv6(ip_address)
        except AddressValueError as e:
            raise ValueError(f'Invalid IPv6 address: {ip_address}')
