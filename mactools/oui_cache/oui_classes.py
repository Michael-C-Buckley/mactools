# OUI Cache Classes

# Python Modules
from datetime import datetime
from enum import Enum
from re import search
from typing import Dict

# Local Modules
from mactools.mac_common import prepare_oui

from mactools.oui_cache.oui_common import (
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
    Singleton for holding the OUI Cache
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, oui_dict: Dict[OUIType, Dict[str, str]]) -> None:
        self.version: str = VERSION
        self.timestamp: datetime = datetime.now()
        self.oui_dict: Dict[OUIType, Dict[str, str]] = oui_dict
        self._initialized = True

    def get_record(self, input_mac: str) -> Dict[str, str]:
        """
        Returns the assigned OUI and organization associated with a MAC or OUI
        """
        oui = prepare_oui(input_mac)

        def check_locally_administered(input_mac: str):
            # Identify a locally administered MAC via U/L of the first byte
            if bin(int(input_mac[:2], 16))[2:].zfill(8)[6] == '1':
                return {'oui': input_mac, 'vendor': 'Locally administered'}

        def check_range(input_mac: str):
            # Check MACs within a set range
            for mac_criteria, info in mac_ranges.items():
                if search(mac_criteria, input_mac):
                    return {'oui': input_mac, 'vendor': info}
                
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
                return {'oui': oui, 'vendor': result}

        key_length_map = {
            OUIType.OUI36: 9,
            OUIType.OUI28: 7,
            OUIType.OUI: 6
        }

        for oui_type, key_len in key_length_map.items():
            inner_dict: Dict[str, str] = self.oui_dict.get(oui_type)
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
        