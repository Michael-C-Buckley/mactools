# MacTools MAC Address Class

# Python Modules
from typing import Union

# Local Modules
from mactools.basemac import BaseMac, MacNotation
from mactools.oui_cache import OUICache, get_oui_cache

oui_cache = get_oui_cache()

class MacAddress(BaseMac):
    """
    Final class that merges `OUICache` instance into the `BaseMac` for
    look-ups automatically on creation and prevents circular dependencies
    """
    def __init__(self, mac: Union[str, int], format: MacNotation = MacNotation.COLON,
                 cache: OUICache = None, *args, **kwargs):
        if cache is None:
            cache = oui_cache
        super().__init__(mac, format, cache)