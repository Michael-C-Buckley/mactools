# OUI Database

# Python Modules
# Local Modules
from mactools.oui_cache.oui_classes import OUICache
from mactools.oui_cache.oui_common import create_oui_dict


def get_oui_cache(regenerate: bool = False) -> OUICache:
    """
    Gets the IEEE OUI info, creates, and pickles the cache
    """
    if OUICache._instance is not None and not regenerate:
        return OUICache._instance

    return OUICache(create_oui_dict())


def get_oui_record(input_mac: str) -> dict[str, str] | None:
    """
    Gets the record of a MAC or OUI
    """
    return get_oui_cache().get_record(input_mac)


def get_oui_vendor(input_mac: str) -> str:
    """
    Gets the vendor names of a MAC or OUI
    """
    return get_oui_cache().get_vendor(input_mac)
