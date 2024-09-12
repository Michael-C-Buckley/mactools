# MacTools MAC Address Class

# Python Modules
from typing import Union

# Local Modules
from mactools.basemac import BaseMac, MacNotation

class MacAddress(BaseMac):
    """
    Final class that merges `OUICache` instance into the `BaseMac` for
    look-ups automatically on creation and prevents circular dependencies.
    """
    def __init__(self, mac: Union[str, int], format: MacNotation = MacNotation.COLON,
                 *args, **kwargs):
        
        # Keyword arguments for cache instances to override default global cache
        input_cache = None
        for keyword in ['cache', 'oui_cache']:
            input_cache = kwargs.get(keyword)
            if input_cache:
                break

        if input_cache is None:
            from mactools.oui_cache import get_oui_cache
            oui_cache = get_oui_cache()

        init_cache = oui_cache if input_cache is None else input_cache
        super().__init__(mac, format, oui_cache=init_cache)