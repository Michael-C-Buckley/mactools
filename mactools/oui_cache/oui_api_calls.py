# OUI Cache API Calls

# Third-Party Libraries
from httpx import get, Response

def httpx_get(resource: str, verify: bool = False) -> Response:
    """"""
    response: Response = get(resource, verify=verify)
    response.raise_for_status()
    return response

def get_oui_text(verify: bool = False) -> Response:
    """
    Pulls down the IEEE OUI Text registry
    """
    return httpx_get('https://standards-oui.ieee.org/oui/oui.txt', verify)


def vendor_oui_lookup(mac: str, verify: bool = False) -> str|None:
    """
    REST request to look-up the OUI of a mac address and returns the vendor.
    URL has a rate limit of 1/s and daily limit of 1000 calls.
    """
    raise NotImplementedError('This method is not yet implemented')
    return  httpx_get(f'http://api.macvendors.com/{mac}', verify)
