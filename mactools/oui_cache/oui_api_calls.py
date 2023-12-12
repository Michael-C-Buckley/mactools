# OUI Cache API Calls

# Python Libraries
from functools import wraps
from json import loads
from os import environ
from typing import Callable, Union, Dict

# Third-Party Libraries
from asyncio_throttle import Throttler
from httpx import AsyncClient, Response 

# Local Libraries
from mactools.basemac import BaseMac
from mactools.oui_cache import OUIType
from mactools.mac_common import fill_hex


# Get 
api_key = environ.get('MACLOOKUP_API_KEY')
rate_limit = 10 if api_key else 2
throttler = Throttler(rate_limit)

client_session = AsyncClient(verify=False, timeout=60)

def prepare_mac(func: Callable, *args) -> Callable:
    """
    Decorator for handling strings or `BaseMac` input variables.
    Pads out strings to create a psuedo-MAC for proper object functioning.
    """
    @wraps(func)
    async def wrapper(func_input: Union[str, BaseMac], *args):
        if not isinstance(func_input, BaseMac):
            func_input = BaseMac(fill_hex(func_input, 12, backfill=True))
        return await func(func_input, *args)
    return wrapper

async def httpx_get(resource: str, client: AsyncClient = None) -> Response:
    """
    Wrapper for `httpx`
    """
    client = client_session if client is None else client
    return await client.get(resource)

async def maclookupapp_get(mac: str, vendor_lookup: bool = True):
    """
    Wrapper for making requests to maclookup.app
    """
    url = f'https://api.maclookup.app/v2/macs/{mac}'
    if vendor_lookup:
        url = f'{url}/company/name'
    if api_key:
        url = f'{url}?apiKey={api_key}'
    async with throttler:
        return await httpx_get(url)

async def get_oui_csv(version: OUIType = OUIType.OUI) -> Response:
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
    return await httpx_get(url)

@prepare_mac
async def vendor_oui_lookup(mac: Union[str, BaseMac]) -> Dict[str, None]:
    """
    REST request to look-up the OUI of a mac address and returns the vendor.
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    return maclookupapp_get(mac)

@prepare_mac
async def mac_lookup_call(mac: Union[str, BaseMac]) -> Dict[str, str]:
    """
    REST request to get OUI info (WIP).
    URL has a rate limit of 2/s and daily limit of 10,000 calls.
    """
    response = await maclookupapp_get(mac, False)
    return loads(response.text)
