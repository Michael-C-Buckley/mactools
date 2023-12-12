# OUI Database

# Python Modules
from asyncio import as_completed, create_task, gather, run
from csv import reader
from io import StringIO
from typing import Callable, Dict, Optional, Union
from pickle import load, loads

# Local Modules
from mactools.version import __version__ as VERSION
from mactools.oui_cache.oui_api_calls import get_oui_csv
from mactools.oui_cache.oui_common import PICKLE_DIR
from mactools.oui_cache.oui_classes import OUICache, OUIType

async def process_ieee_csv(csv: str) -> Dict[OUIType, Dict[str, str]]:
    """
    Converts the IEEE CSV response into a Python dictionary
    """
    csv_reader = reader(StringIO(csv))
    entries = {}

    # Skip the IEEE header line
    next(csv_reader)

    for record in csv_reader:
        assignment_type, oui, vendor, address = record
        entries[oui] = vendor

    return {OUIType(assignment_type): entries}

async def build_oui_cache(save_cache: bool = True) -> Optional[OUICache]:
    """
    Gets the IEEE OUI info, creates, and pickles the cache
    """
    print('MacTools: Fetching IEEE files...', end='\r')
    coroutines = [create_task(get_oui_csv(i)) for i in OUIType]

    oui_dict = {}
    for task in as_completed(coroutines):
        response = await task
        if response.status_code == 200:
            oui_dict.update(await process_ieee_csv(response.text))
        else:
            print('MacTools: Failed to get IEEE file.')
            return None

    OUICache._instance = None        
    oui_cache = OUICache(oui_dict)
    if save_cache:
        await oui_cache.aio_write_oui_cache()

    print('MacTools: IEEE files successfully obtained.')

    return oui_cache

def check_cache(load_func: Callable, data):
    oui_cache: OUICache = load_func(data)
    if isinstance(oui_cache.version, str):
        if VERSION == oui_cache.version:
            return oui_cache
    raise ValueError('The cache is not valid')

def get_oui_cache(rebuild: bool = False, save_cache: bool = True,
                        bypass: bool = False) -> OUICache:
    """
    Retrieves local instance or creates a new `OUICache`
    """
    if not rebuild:
        if OUICache._instance and VERSION == OUICache._instance.version:
            return OUICache()
        try:
            with open(PICKLE_DIR, 'rb') as file:
                return check_cache(load, file)
        except Exception as e:
           pass

    if bypass:
        return None
    
    return run(build_oui_cache(save_cache))

def get_oui_vendor(input_item: Union[str, list[str]]) -> str:
    """
    Sync wrapper for getting OUI vendor/company name
    """
    return run(aio_get_oui_vendor(input_item))

async def aio_get_oui_cache(rebuild: bool = False, save_cache: bool = True,
                        bypass: bool = False) -> OUICache:
    """
    Async retrieval local or create new `OUICache`
    """
    if not rebuild:
        if OUICache._instance and VERSION == OUICache._instance.version:
            return OUICache()
        try:
            from mactools.oui_cache.oui_common import oui_pickle_task
            return check_cache(loads, await oui_pickle_task)
        except Exception as e:
            pass

    if bypass:
        return None
    
    return await build_oui_cache(save_cache)

async def aio_get_oui_item(input_item: Union[str, list[str]],
                 func: Callable) -> Optional[Union[str, list[str]]]:
    """
    Inner function for `get_oui_vendor` and `get_oui_record`
    """
    if isinstance(input_item, str):
        return await func(input_item.upper())
    elif isinstance(input_item, list):
        result = []
        for item in input_item:
            if isinstance(item, str):
                result.append(func(item.upper()))
            else:
                raise ValueError('The input list must be strings')
            await gather(*result)
        return result
    raise ValueError('Input must be either a string or list of strings')

async def aio_get_oui_vendor(input_item: Union[str, list[str]],
                   rebuild: bool = False) -> str:
    """
    Simple function to request the vendor from a MAC/OUI or a list of them
    """
    if not OUICache._instance:
        pass
    oui_cache = await aio_get_oui_cache(rebuild)
    return aio_get_oui_item(input_item, oui_cache.get_vendor)

async def aio_get_oui_record(input_item: Union[str, list],
                   rebuild: bool = False) -> Dict[str, str]:
    """
    Simple function to request `OUIRecord` from a MAC/OUI or a list of them
    """
    oui_cache = await aio_get_oui_cache(rebuild)
    return aio_get_oui_item(input_item, oui_cache.get_record)
