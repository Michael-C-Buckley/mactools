# OUI Cache Classes

# Python Modules
from dataclasses import dataclass
from datetime import datetime
from os import makedirs
from pickle import dump
from re import search
from typing import Dict, Optional

# Local Modules
from mactools.oui_cache.oui_common import (
    CACHE_DIR,
    PICKLE_DIR,
    VERSION,
    fixed_ouis,
    specific_macs,
    mac_ranges
)

from mactools.mac_common import prepare_oui

@dataclass
class OUIRecord:
    oui: str
    vendor: str
    hex_oui: str = None
    street_address: str = None
    city: str = None
    state: str = None
    postal_code: str = None
    country: str = None


class OUICache:
    """
    Object holding the OUI Cache
    """
    def __init__(self, oui_dict: Dict[str, OUIRecord]):
        """
        Cache Objection - Version is the library version.
        """
        self.cache_version: str = VERSION
        self.timestamp: datetime = datetime.now()
        self.oui_dict: Dict[str, OUIRecord] = oui_dict
    
    def get_record(self, input_mac: str) -> Optional[OUIRecord]:
        """
        Returns a single `OUIRecord`
        """
        oui = prepare_oui(input_mac)

        def check_range(input_mac: str):
            for mac_criteria, info in mac_ranges.items():
                if search(mac_criteria, input_mac):
                    return info

        func_dict = {
            specific_macs.get: input_mac,
            fixed_ouis.get: input_mac,
            check_range: input_mac,
            self.oui_dict.get: oui
        }

        for func, input_val in func_dict.items():
            result = func(input_val)
            if result:
                if not isinstance(result, OUIRecord):
                    result = OUIRecord(oui, result)
                return result

    def get_vendor(self, oui: str) -> Optional[str]:
        """
        Returns the vendor of an OUI
        """
        record = self.get_record(oui)
        if record:
            return record.vendor
    
    # File handling
    def write_oui_cache(self) -> None:
        """
        Writes `OUICache` object to the user's cache directory
        """
        makedirs(CACHE_DIR, exist_ok=True)
        with open(PICKLE_DIR, 'wb') as file:
            dump(self, file)
