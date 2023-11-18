# MacTools MAC Address Class

from mactools.basemac import BaseMac, MacNotation
from mactools.oui_cache.oui_core import OUICache, get_oui_cache

class MacAddress(BaseMac):
    """
    Final class that merges `OUICache` instance into the `BaseMac` for
    look-ups automatically on creation and prevents circular dependencies
    """
    def __init__(self, mac: str | int, format: MacNotation = MacNotation.COLON,
                 oui_cache: OUICache = None):
        if not oui_cache:
            oui_cache = get_oui_cache()
        super().__init__(mac, format, oui_cache)
