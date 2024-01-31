# OUI Cache API Calls

# Python Libraries
from typing import Union, Dict
from urllib.request import urlopen


# Local Libraries
from mactools.basemac import BaseMac
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

@prepare_mac
def vendor_oui_lookup(mac: Union[str, BaseMac]) -> Dict[str, None]:
    """
    REST request to look-up the OUI of a mac address and returns the vendor.
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    url = f'https://api.maclookup.app/v2/macs/{mac.clean}/company/name'
    with urlopen(url) as response:
        response_text = response.read().decode('utf-8')
    return response_text