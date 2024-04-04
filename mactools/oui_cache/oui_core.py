# OUI Database

# Python Modules
from csv import reader
from concurrent.futures import ThreadPoolExecutor as Executor
from pkg_resources import resource_filename
from os import path
from typing import Dict, Optional, Union

# Local Modules
from mactools.oui_cache.oui_classes import OUICache, OUIType
from mactools.update_ieee import update_ieee_files

def process_ieee_csv(file_path: str) -> Dict[OUIType, Dict[str, str]]:
    """
    Converts the IEEE CSV response into a Python dictionary
    """
    with open(file_path, encoding='utf-8') as file:
        csv = reader(file)
        next(csv)

        entries = {}
        for record in csv:
            assignment_type, oui, vendor, address = record
            entries[oui] = {'vendor': vendor, 'oui': oui, 'address': address}

    return {OUIType(assignment_type): entries}

def get_oui_cache(regenerate: bool = False) -> OUICache:
    """
    Gets the IEEE OUI info, creates, and pickles the cache
    """
    if OUICache._instance is not None and not regenerate:
        return OUICache._instance

    base_path = resource_filename('mactools', 'resources/ieee')
    file_paths = [path.join(base_path, f'{i}.csv') for i in ['oui36', 'mam', 'oui']]
    for file_path in file_paths:
        if not path.exists(file_path):
            update_ieee_files()
            break

    with Executor(max_workers=3) as executor:
        oui_dicts = executor.map(process_ieee_csv, file_paths)

    final_dict = {}
    for oui_dict in oui_dicts:
        final_dict.update(oui_dict)

    return OUICache(final_dict)

def get_oui_record(input_mac: str) -> Optional[dict[str, str]]:
    """
    Gets the record of a MAC or OUI
    """
    return get_oui_cache().get_record(input_mac)

def get_oui_vendor(input_mac: str) -> str:
    """
    Gets the vendor names of a MAC or OUI
    """
    return get_oui_cache().get_vendor(input_mac)