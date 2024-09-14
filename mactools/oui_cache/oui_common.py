# Pytho Modules
from concurrent.futures import ThreadPoolExecutor as Executor
from csv import reader
from enum import Enum
from io import StringIO
from os import path
from importlib.resources import files
from typing import Dict, TYPE_CHECKING


# Common Re-used Imports
from mactools import __version__ as VERSION

# Local Modules
from mactools.update_ieee import update_ieee_files

if TYPE_CHECKING:
    from mactools.oui_cache.oui_classes import OUIType

BASE_IEEE_PATH = files('mactools').joinpath('resources/ieee')
IEEE_FILE_PATHS = [path.join(BASE_IEEE_PATH, f'{i}.csv') for i in ['oui36', 'mam', 'oui']]

# Flag to mark the cache for update immediately when the cache is invalidated
UPDATE_IEEE = True


class OUIType(Enum):
    """
    Differentiator for IEEE MAC OUI Registry sizes
    """
    OUI36 = 'MA-S'
    OUI28 = 'MA-M'
    OUI = 'MA-L'


fixed_ouis: dict[str, str] = {
    'FFFFFF': 'Broadcast',
    '0180C2': 'STP/LLDP/CFM',
    '01005E': 'IPv4 Multicast',
    '01000C': 'Cisco CDP/PAgP/VTP/DTP/UDLD',
    '011B19': 'Precision Time Protocol (PTP)',
}

specific_macs: dict[str, str] = {
    'FFFFFFFFFFFF': 'Broadcast',
    '0180C200000E': 'Link Layer Discovery Protocol (LLDP)',
    '01000CCCCCAB': 'Cisco UniDirectional Link Detection (UDLD)',
    '01000CCCCCCC': 'Cisco CDP/VTP/DTP',
    '01000CCCCCAA': 'Cisco Port Aggregation Protocol (PAgP)',
    '00E02B000004': 'Extreme Networks Standby Protocol'
}

mac_ranges: dict[str, str] = {
    r'3333[0-9A-Fa-f]{2}': 'IPv6 Multicast',
    r'0180C200000[0-9A-Fa-f]': 'Spanning Tree Protocol (STP)',
    r'00005E0001[0-9A-Fa-f]{2}': 'Virtual Router Redundancy Protocol (VRRP)',
    r'00000C07AC[0-9A-Fa-f]{2}': 'Cisco HSRP/GLBP',
}


def process_ieee_csv(file_path: str) -> Dict[OUIType, Dict[str, str]]:
    """
    Converts the IEEE CSV response into a Python dictionary
    """
    try:
        with open(file_path, encoding='utf-8') as file:
            contents = StringIO(file.read())
    except FileNotFoundError:
        update_ieee_files()
        return process_ieee_csv(file_path)

    records = reader(contents)

    # Skip IEEE's header, StopIteration means the file was empty
    try:
        next(records)
    except StopIteration:
        update_ieee_files()
        return process_ieee_csv(file_path)

    entries = {}
    for record in records:
        assignment_type, oui, vendor, address = record
        entries[oui] = {'vendor': vendor, 'oui': oui, 'address': address}

    return {OUIType(assignment_type): entries}

def create_oui_dict(update: bool = False) -> Dict['OUIType', Dict[str, str]]:
    """
    Creates the dictionary used in the cache object from the IEEE CSV files
    """
    if update is True:
        update_ieee_files()
        
    for file_path in IEEE_FILE_PATHS:
        if not path.exists(file_path):
            update_ieee_files(overwrite=False)

    for file_path in IEEE_FILE_PATHS:
        process_ieee_csv(file_path)

    with Executor(max_workers=3) as executor:
        oui_dicts = executor.map(process_ieee_csv, IEEE_FILE_PATHS)

    final_dict = {}
    for oui_dict in oui_dicts:
        final_dict.update(oui_dict)
    
    return final_dict