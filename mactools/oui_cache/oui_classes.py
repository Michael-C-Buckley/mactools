# OUI Cache Classes

# Python Modules
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from os import makedirs
from pickle import dump

# Local Modules
from mactools.oui_cache.oui_common import (
    CACHE_DIR,
    PICKLE_DIR,
    MacAddress,
    VERSION
)

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
    
    def prepare_oui(func: callable) -> callable:
        """
        Takes a MAC or OUI and strips and prepares a unified clean OUI
        """
        def wrapper(self, func_input: Union[MacAddress, str]) -> Any:
            if isinstance(func_input, str):
                oui = MacAddress.clean_mac_address(func_input)[0:6].upper()
            elif isinstance(func_input, MacAddress):
                oui = func_input.clean_oui
            return func(self, oui)
        return wrapper
    
    @prepare_oui
    def get_record(self, oui: str) -> Optional[OUIRecord]:
        """
        Returns a single `OUIRecord`
        """
        return self.oui_dict.get(oui)
    
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
            from icecream import ic
            ic(PICKLE_DIR)
            dump(self, file)