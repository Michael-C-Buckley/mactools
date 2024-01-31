# OUI Database

# Python Modules
from csv import reader
from concurrent.futures import ThreadPoolExecutor as Executor
from pkg_resources import resource_filename
from os import path
from typing import Dict, Optional, Union

# Local Modules
from mactools.oui_cache.oui_classes import OUICache, OUIType

def process_ieee_csv(file_path: str) -> Dict[OUIType, Dict[str, str]]:
    """
    Converts the IEEE CSV response into a Python dictionary
    """
    with open(file_path) as file:
        csv = reader(file)
        next(csv)

        entries = {}
        for record in csv:
            assignment_type, oui, vendor, address = record
            entries[oui] = vendor

    return {OUIType(assignment_type): entries}

def get_oui_cache() -> OUICache:
    """
    Gets the IEEE OUI info, creates, and pickles the cache
    """
    if OUICache._instance is not None:
        return OUICache._instance

    with Executor(max_workers=3) as executor:
        base_path = resource_filename('mactools', 'resources/ieee')
        paths = [path.join(base_path, f'{i}.csv') for i in ['oui36', 'mam', 'oui']]
        oui_dicts = executor.map(process_ieee_csv, paths)

    final_dict = {}
    for oui_dict in oui_dicts:
        final_dict.update(oui_dict)

    return OUICache(final_dict)

def get_oui_vendor(input_item: Union[str, list[str]]) -> Optional[Union[str, list[str]]]:
    """
    Gets the vendor names of the passed string or list of strings
    """
    oui_cache = get_oui_cache()
    if isinstance(input_item, str):
        return oui_cache.get_vendor(input_item.upper())
    elif isinstance(input_item, list):
        result = []
        for item in input_item:
            if isinstance(item, str):
                result.append(oui_cache.get_vendor(item.upper()))
            else:
                raise ValueError('The input list must be strings')
        return result
    raise ValueError('Input must be either a string or list of strings')