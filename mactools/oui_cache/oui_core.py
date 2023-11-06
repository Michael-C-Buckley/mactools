# OUI Database

# Python Modules
from io import StringIO
from typing import Dict, Optional, Union
from pickle import load

# Third-Party Modules
from textfsm import TextFSM

# Local Modules
from mactools.version import __version__ as VERSION
from mactools.oui_cache.oui_api_calls import get_oui_text
from mactools.oui_cache.oui_template import OUI_TEMPLATE
from mactools.oui_cache.oui_classes import OUICache, OUIRecord
from mactools.oui_cache.oui_common import PICKLE_DIR


def build_oui_cache(save_cache: bool = True) -> Optional[OUICache]:
    """
    Gets the IEEE OUI Text and creates the pickle the cache
    """
    print('OUI: Fetching IEEE file...')
    oui_response = get_oui_text()
    if oui_response.status_code != 200:
        return None
    
    template = TextFSM(StringIO(OUI_TEMPLATE))
    output = template.ParseTextToDicts(oui_response.text)

    oui_dict: Dict[str, OUIRecord] = {}

    for item in output:
        oui = item['oui']
        oui_dict[oui] = OUIRecord(**item)

    oui_cache = OUICache(oui_dict)
    if save_cache:
        oui_cache.write_oui_cache()

    # ADD FIXED MACS

    return oui_cache

def get_oui_cache(rebuild: bool = False, save_cache: bool = True) -> OUICache:
    """
    Retrieve local or create new `OUICache`
    """
    if not rebuild:
        try:
            with open(PICKLE_DIR, 'rb') as file:
                oui_cache: OUICache = load(file)
                if isinstance(oui_cache.cache_version, str):
                    if VERSION == oui_cache.cache_version:
                        return oui_cache
        except (AttributeError, FileNotFoundError):
            pass
    
    return build_oui_cache(save_cache)

def get_oui_item(input_item: Union[str, list[str]],
                 func: callable) -> Optional[Union[str, list[str]]]:
    """
    Inner function for `get_oui_vendor` and `get_oui_record`
    """
    if isinstance(input_item, str):
        return func(input_item.upper())
    elif isinstance(input_item, list):
        result = []
        for item in input_item:
            if isinstance(item, str):
                result.append(func(item.upper()))
            else:
                raise ValueError('The input list must be strings')
        return result
    raise ValueError('Input must be either a string or list of strings')

def get_oui_vendor(input_item: Union[str, list[str]],
                   rebuild: bool = False) -> Optional[str]:
    """
    Simple function to request the vendor from a MAC/OUI or a list of them
    """
    oui_cache = get_oui_cache(rebuild)
    return get_oui_item(input_item, oui_cache.get_vendor)

def get_oui_record(input_item: Union[str, list],
                   rebuild: bool = False) -> Optional[OUIRecord]:
    """
    Simple function to request `OUIRecord` from a MAC/OUI or a list of them
    """
    oui_cache = get_oui_cache(rebuild)
    return get_oui_item(input_item, oui_cache.get_record)
