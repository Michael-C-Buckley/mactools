# OUI Cache API Calls

# Python Libraries
from json import loads
from typing import Union

# Third-Party Libraries
from httpx import get, Response

# Local Libraries
from mactools.macaddress import MacAddress
from mactools.oui_cache.oui_classes import OUIRecord
from mactools.mac_common import fill_hex


def prepare_mac(func: callable, *args) -> callable:
    """
    Decorator for handling strings or `MacAddress` input variables.
    Pads out strings to create a psuedo-MAC for proper object functioning.
    """
    def wrapper(func_input: Union[str, MacAddress], *args):
        if not isinstance(func_input, MacAddress):
            func_input = MacAddress(fill_hex(func_input, 12, backfill=True))
        return func(func_input, *args)
    return wrapper

def httpx_get(resource: str, verify: bool = False, timeout: float = 10) -> Response:
    """
    Wrapper for `httpx`
    """
    response: Response = get(resource, verify=verify, timeout=timeout)
    response.raise_for_status()
    return response

def get_oui_text(verify: bool = False) -> Response:
    """
    Pulls down the IEEE OUI Text registry
    """
    ieee_oui_url = 'https://standards-oui.ieee.org/oui/oui.txt'
    return httpx_get(ieee_oui_url, verify, timeout=30)

@prepare_mac
def vendor_oui_lookup(mac: Union[str, MacAddress], verify: bool = False) -> str|None:
    """
    REST request to look-up the OUI of a mac address and returns the vendor.
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    return  httpx_get(f'https://api.maclookup.app/v2/macs/{mac.clean}/company/name', verify)

@prepare_mac
def mac_lookup_call(mac: Union[str, MacAddress], verify: bool = False):
    """
    REST request to get OUI info (WIP).
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    response = httpx_get(f'https://api.maclookup.app/v2/macs/{mac.clean}', verify)
    payload: dict[str, str] = loads(response.text)

    record_dict = {
        'oui': payload.get('macPrefix'),
        'vendor': payload.get('company'),
    }
    return OUIRecord(**record_dict)
