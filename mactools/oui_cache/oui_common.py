# Python Modules
from aiofiles import open as aio_open
from asyncio import create_task
from os import path

# Third Party Modules
from appdirs import user_data_dir

# Common Re-used Imports
from mactools import __version__ as VERSION

# Cache file constants
CACHE_DIR = user_data_dir()
PICKLE_DIR = path.join(CACHE_DIR, 'oui.pkl')
oui_pickle_task = None

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

async def open_pickle():
    """
    Coroutine to work in conjunction with `create_pickle_task` to expedite
    loading by scheduling file IO early
    """
    try:
        async with aio_open(PICKLE_DIR, 'rb') as file:
            return await file.read()
    except Exception as e:
        return e
    
async def create_pickle_task():
    """
    Scheduler for loading the cache pickle file
    """
    global oui_pickle_task
    oui_pickle_task = create_task(open_pickle())