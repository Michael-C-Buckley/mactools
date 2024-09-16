# OUI Cache Classes

# Python Modules
from datetime import datetime
from json import load
from re import search
from time import sleep
from typing import Dict
from urllib.request import urlopen

# Local Modules
from mactools.mac_common import prepare_oui
from mactools.tools_common import get_hex_value

from mactools.oui_cache.oui_common import (
    VERSION, OUIType, create_oui_dict,
    fixed_ouis, specific_macs, mac_ranges,
    UPDATE_IEEE
)
    

class OUICache:
    """
    Singleton for holding the OUI Cache
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    @classmethod
    def replace_instance(cls, new):
        """"""
        cls._instance = new
    
    def __init__(self, oui_dict: Dict[OUIType, Dict[str, str]], attempt_update: bool = True) -> None:
        self.attempt_update = attempt_update
        self.version: str = VERSION
        self.timestamp: datetime = datetime.now()
        self.oui_dict: Dict[OUIType, Dict[str, str]] = oui_dict
        self._initialized = True

    def get_record(self, input_mac: str) -> Dict[str, str]:
        """
        Returns the assigned OUI and organization associated with a MAC or OUI
        """
        oui = prepare_oui(input_mac)

        hex_value = get_hex_value(oui)
        if hex_value == -1:
            return {'input': input_mac, 'error': True, 'note': 'This is not a valid hex string'}
        if hex_value < 24:
            return {'input': input_mac, 'error': True, 'note': 'OUI/MAC is shorter than 6 hex characters (24 bits) and too short to be any OUI'}
        if hex_value > 64:
            return {'input': input_mac, 'error': True, 'note': 'OUI/MAC is longer than 16 hex characters (64 bits) and longer than MAC addresses can be'}

        base_dict = {
            'oui': input_mac,
            'error': False,
        }
        
        def check_locally_administered(input_mac: str):
            # Identify a locally administered MAC via U/L of the first byte
            if bin(int(input_mac[:2], 16))[2:].zfill(8)[6] == '1':
                base_dict['vendor'] = 'Locally administered'
                return base_dict
                

        def check_range(input_mac: str):
            # Check MACs within a set range
            for mac_criteria, info in mac_ranges.items():
                if search(mac_criteria, input_mac):
                    base_dict['vendor'] = info
                    return base_dict
                
        func_dict = {
            specific_macs.get: oui,
            fixed_ouis.get: oui[:6],
            check_range: oui,
            check_locally_administered: oui,
        }

        for func, input_mac in func_dict.items():
            result = func(input_mac)
            if isinstance(result, dict):
                return result
            elif isinstance(result, str):
                base_dict['vendor'] = result
                return base_dict

        key_length_map = {
            OUIType.OUI36: 9,
            OUIType.OUI28: 7,
            OUIType.OUI: 6
        }

        for oui_type, key_len in key_length_map.items():
            inner_dict: Dict[str, str] = self.oui_dict.get(oui_type)
            result = inner_dict.get(oui[:key_len])
            if result:
                result['error'] = False
                return result
            
        # Check to see if the record exists but isn't in the cache, in which trigger an update
        with urlopen(f'https://api.maclookup.app/v2/macs/{input_mac}') as response:

            # Fall-through case for valid OUI without any registration
            no_entry_note = 'This OUI is valid but has no associated registration in the IEEE global registry (MA-L, MA-M, or MA-S)'
            no_entry_dict = {'oui': oui,
                            'vendor': 'Unregistered',
                            'note': no_entry_note,
                            }
            
            # Stateless delay to prevent 429 from the endpoint
            sleep(0.5)

            if response.code == 200:
                result = load(response)
                
                if result['success'] != True:
                    
                    return no_entry_dict

                # Update the entire cache due to invalidation
                if UPDATE_IEEE is True:
                    self.oui_dict = create_oui_dict(update=True)

                if result['found'] != True:
                    return no_entry_dict

                api_oui = result['macPrefix']
                vendor = result['company']

                # Add it to the run-time cache of which assumes MA-L entries currently
                # This is chosen when not completely updating the whole cache
                if UPDATE_IEEE is False:
                    self.oui_dict[OUIType('MA-L')][api_oui] = {
                        'vendor' : vendor,
                        'oui': api_oui,
                        'address': result['address'],
                    }

                return {'oui': api_oui, 'vendor': vendor}
        
            
    def get_vendor(self, input_mac: str) -> str:
        """
        Returns the organization associated with an assignment
        """
        record_dict = self.get_record(input_mac)
        if record_dict:
            if record_dict.get('error'):
                raise ValueError(record_dict['error'])
            return record_dict.get('vendor')