# OUI Cache Classes

# Python Modules
from datetime import datetime
from enum import Enum
from os import makedirs
from pickle import dump
from re import search
from typing import Dict

# Local Modules
from mactools.mac_common import prepare_oui

from mactools.oui_cache.oui_common import (
    CACHE_DIR,
    PICKLE_DIR,
    VERSION,
    fixed_ouis,
    specific_macs,
    mac_ranges
)


class OUIType(Enum):
    """
    Differentiator for IEEE MAC OUI Registry sizes
    """
    OUI36 = 'MA-S'
    OUI28 = 'MA-M'
    OUI = 'MA-L'
    

class OUICache:
    """
    Object for holding the OUI Cache
    """
    def __init__(self, oui_dict: Dict[OUIType, Dict[str, str]]) -> None:
        self.version: str = VERSION
        self.timestamp: datetime = datetime.now()
        self.oui_dict: Dict[OUIType, Dict[str, str]] = oui_dict

    def get_record(self, input_mac: str) -> Dict[str, str]:
        """
        Returns the assigned OUI and organization associated with a MAC or OUI
        """
        oui = prepare_oui(input_mac)

        def check_range(input_mac: str):
            for mac_criteria, info in mac_ranges.items():
                if search(mac_criteria, input_mac):
                    return {'oui': input_mac, 'vendor': info}
                
        func_dict = {
            specific_macs.get: oui,
            fixed_ouis.get: oui[:6],
            check_range: oui,
        }

        for func, input_mac in func_dict.items():
            result = func(input_mac)
            if result:
                return result

        key_length_map = {
            OUIType.OUI36: 9,
            OUIType.OUI28: 7,
            OUIType.OUI: 6
        }

        for oui_type, key_len in key_length_map.items():
            inner_dict: Dict[str, str] = self.oui_dict.get(oui_type)
            if inner_dict is None:
                continue
            result = inner_dict.get(oui[:key_len])
            if result:
                return {'oui': oui[:key_len], 'vendor': result}
            
    def get_vendor(self, input_mac: str) -> str:
        """
        Returns the organization associated with an assignment
        """
        record_dict = self.get_record(input_mac)
        if record_dict:
            return record_dict.get('vendor')
        
    # File handling
    def write_oui_cache(self) -> None:
        """
        Writes `OUICache` object to the user's cache directory
        """
        makedirs(CACHE_DIR, exist_ok=True)
        with open(PICKLE_DIR, 'wb') as file:
            dump(self, file)
