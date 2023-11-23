# OUI Database

# Python Modules
from csv import reader
from concurrent.futures import ThreadPoolExecutor as Executor
from io import StringIO
from typing import Dict, Optional, Union
from pickle import load

# Local Modules
from mactools.version import __version__ as VERSION
from mactools.oui_cache.oui_api_calls import get_oui_csv
from mactools.oui_cache.oui_classes import OUICache, OUIType
from mactools.oui_cache.oui_common import PICKLE_DIR


def process_ieee_csv(csv: str) -> Dict[OUIType, Dict[str, str]]:
    """
    Converts the IEEE CSV response into a Python dictionary
    """
    csv_reader = reader(StringIO(csv))
    entries = {}

    # Skip the IEEE header line
    next(csv_reader)

    for record in csv_reader:
        assignment_type, oui, vendor, address = record
        entries[oui] = vendor

    return {OUIType(assignment_type): entries}

def build_oui_cache(save_cache: bool = True) -> Optional[OUICache]:
    """
    Gets the IEEE OUI info, creates, and pickles the cache
    """
    print('MacTools: Fetching IEEE info...', end='\r')

    with Executor(max_workers=3) as executor:
        results = executor.map(get_oui_csv, OUIType)

    oui_dict = {}
    for response in results:
        if response.status_code == 200:
            oui_dict.update(process_ieee_csv(response.text))
        else:
            print('MacTools: Failed to get IEEE file.')
            return None
        

    print('MacTools: IEEE info successfully obtained.')

    oui_cache = OUICache(oui_dict)
    if save_cache:
        oui_cache.write_oui_cache()

    return oui_cache

def get_oui_cache(rebuild: bool = False, save_cache: bool = True) -> OUICache:
    """
    Retrieve local or create new `OUICache`
    """
    if not rebuild:
        try:
            with open(PICKLE_DIR, 'rb') as file:
                oui_cache: OUICache = load(file)
                if isinstance(oui_cache.version, str):
                    if VERSION == oui_cache.version:
                        return oui_cache
        except Exception as e:
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
                   rebuild: bool = False) -> str:
    """
    Simple function to request the vendor from a MAC/OUI or a list of them
    """
    oui_cache = get_oui_cache(rebuild)
    return get_oui_item(input_item, oui_cache.get_vendor)

def get_oui_record(input_item: Union[str, list],
                   rebuild: bool = False) -> Dict[str, str]:
    """
    Simple function to request `OUIRecord` from a MAC/OUI or a list of them
    """
    oui_cache = get_oui_cache(rebuild)
    return get_oui_item(input_item, oui_cache.get_record)
