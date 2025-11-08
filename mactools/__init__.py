# MacTools Exposed Imports

from mactools.mac_common import (create_random_hex_bit,
                                 create_random_hex_string, create_random_mac,
                                 fill_hex, hex_range, prepare_oui)
from mactools.macaddress import MacAddress, MacNotation
from mactools.oui_cache.oui_classes import OUICache
from mactools.oui_cache.oui_common import UPDATE_IEEE
from mactools.oui_cache.oui_core import (get_oui_cache, get_oui_record,
                                         get_oui_vendor)
from mactools.update_ieee import update_ieee_files
from mactools.version import __version__

# Try to update IEEE files on first import if they don't exist
try:
    import os
    from importlib.resources import files

    ieee_dir = str(files("mactools") / "resources" / "ieee")
    if os.path.exists(ieee_dir) and not any(
        f.endswith(".csv")
        for f in os.listdir(ieee_dir)
        if os.path.isfile(os.path.join(ieee_dir, f))
    ):
        update_ieee_files(overwrite=True)
except Exception:
    # If update fails, continue anyway - package can still work with cached data
    pass
