from mactools.oui_cache.oui_core import get_oui_record, get_oui_cache

from icecream import ic

record = get_oui_record('6026aa')
ic(record)