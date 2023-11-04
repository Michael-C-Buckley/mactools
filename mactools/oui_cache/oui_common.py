# Python Modules
from os import path as os_path
from sys import path as sys_path
from typing import Union

# Third Party Modules
from appdirs import user_data_dir

# Add the project directory to sys.path
sys_path.append(os_path.dirname(os_path.dirname(os_path.dirname(os_path.abspath(__file__)))))

# Common Re-used Imports
from version import __version__ as VERSION

# Cache file constants base, file will also include the Cache type
CACHE_DIR = user_data_dir('python3-mactools')
PICKLE_DIR = os_path.join(CACHE_DIR, 'oui.pkl')

fixed_ouis: dict[str, str] = {
    'FFFFFF': 'Broadcast',
    '0180C2': 'STP/LLDP/CFM',
    '01005E': 'IPv4 Multicast',
    '01000C': 'Cisco CDP/PAgP/VTP/DTP/UDLD',
    '011B19': 'Precision Time Protocol (PTP)',
}

specific_macs: dict[str, str] = {
    '0180C200000E': 'Link Layer Discovery Protocol',
    '01000CCCCCAB': 'Cisco UniDirectional Link Detection',
    '01000CCCCCCC': 'Cisco CDP/VTP/DTP',
    '01000CCCCCAA': 'Cisco Port Aggregation Protocol',
    '00E02B000004': 'Extreme Networks Standby Protocol'
}

mac_ranges: dict[str, str] = {
    r'3333[0-9A-Fa-f]{2}': 'IPv6 Multicast',
    r'0180C200000[0-9A-Fa-f]': 'Spanning Tree Protocol (STP)',
    r'00005E0001[0-9A-Fa-f]{2}': 'Virtual Router Redundancy Protocol',
    r'00000C07AC[0-9A-Fa-f]{2}': 'Cisco HSRP/GLBP',
}