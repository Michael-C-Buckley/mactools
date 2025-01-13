# Pytho Modules
from concurrent.futures import ThreadPoolExecutor as Executor
from csv import reader
from enum import Enum
from io import StringIO
from os import path, remove
from importlib.resources import files
from tempfile import gettempdir
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



def handle_paths():
    """
    Check to see which paths are writeable for the IEEE CSV files.
    First preference is the library's folder
    Fallback is the temporary files of the computer
    """
    # Constructs to create and track the file paths and statuses
    create_file_paths = lambda x: [path.join(x, f'{i}.csv') for i in ['oui36', 'mam', 'oui']]
    base_ieee_path = files('mactools').joinpath('resources/ieee')
    temp_ieee_path = path.join(gettempdir(), 'python3-mactools')

    library_path_list = create_file_paths(base_ieee_path)
    temp_path_list = create_file_paths(temp_ieee_path)

    path_status = {
        "library": None,
        "temp": None,
    }

    local_list = [(library_path_list, "library"), (temp_path_list, "temp")]

    # Check to see those constructed pathes
    for ieee_path, which_path in local_list:
        for file_path in (ieee_path):
            if not path.exists(file_path):
                path_status[which_path] = False
                break
            else:
                path_status[which_path] = True

    # A hit on either means we have files
    if path_status['library']:
        return library_path_list
    if path_status['temp']:
        return temp_path_list
    
    # No hits prompts a writeable check
    try:
        test_file = path.join(base_ieee_path, 'writetest')
        with open(test_file, 'w') as file:
            file.write('This is only a test')
        remove(test_file)
    except IOError:
        # Library path not writeable, use the temp directory
        return temp_path_list
    
    return library_path_list


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

    file_paths = handle_paths()
        
    for file_path in file_paths:
        if not path.exists(file_path):
            update_ieee_files(overwrite=False)

    for file_path in file_paths:
        process_ieee_csv(file_path)

    with Executor(max_workers=3) as executor:
        oui_dicts = executor.map(process_ieee_csv, file_paths)

    final_dict = {}
    for oui_dict in oui_dicts:
        final_dict.update(oui_dict)
    
    return final_dict