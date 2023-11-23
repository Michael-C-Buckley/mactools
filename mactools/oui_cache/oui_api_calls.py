# OUI Cache API Calls

# Python Libraries
from json import loads
from typing import Union, Dict

# Third-Party Libraries
from httpx import get, Response

# Local Libraries
from mactools.basemac import BaseMac
from mactools.oui_cache import OUIType
from mactools.mac_common import fill_hex


def prepare_mac(func: callable, *args) -> callable:
    """
    Decorator for handling strings or `BaseMac` input variables.
    Pads out strings to create a psuedo-MAC for proper object functioning.
    """
    def wrapper(func_input: Union[str, BaseMac], *args):
        if not isinstance(func_input, BaseMac):
            func_input = BaseMac(fill_hex(func_input, 12, backfill=True))
        return func(func_input, *args)
    return wrapper

def httpx_get(resource: str, verify: bool = False, timeout: float = 10) -> Response:
    """
    Wrapper for `httpx`
    """
    response: Response = get(resource, verify=verify, timeout=timeout)
    response.raise_for_status()
    return response

def get_oui_csv(version: OUIType = OUIType.OUI, verify: bool = False):
    """
    Pulls down the CSV version of the appropriate IEEE standard in CSV form
    """
    base_url = 'https://standards-oui.ieee.org/'
    url_map = {
        OUIType.OUI: 'oui/oui.csv',
        OUIType.OUI28: 'oui28/mam.csv',
        OUIType.OUI36: 'oui36/oui36.csv'
    }
    url = f'{base_url}{url_map.get(version, OUIType.OUI)}'
    return httpx_get(url, verify, timeout=60)

@prepare_mac
def vendor_oui_lookup(mac: Union[str, BaseMac], verify: bool = False) -> Dict[str, None]:
    """
    REST request to look-up the OUI of a mac address and returns the vendor.
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    return  httpx_get(f'https://api.maclookup.app/v2/macs/{mac.clean}/company/name', verify)

@prepare_mac
def mac_lookup_call(mac: Union[str, BaseMac], verify: bool = False) -> Dict[str, str]:
    """
    REST request to get OUI info (WIP).
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    response = httpx_get(f'https://api.maclookup.app/v2/macs/{mac.clean}', verify)
    return loads(response.text)
