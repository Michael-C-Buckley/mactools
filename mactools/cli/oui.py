# MacTools OUI look-up CLI

# Python Modules
from asyncio import run
from argparse import ArgumentParser

#Local Modules
from mactools import MacAddress, MacNotation, aio_get_oui_cache
from mactools.oui_cache.oui_api_calls import mac_lookup_call
from mactools.oui_cache.oui_common import create_pickle_task

help_str = 'Organizationally Unique Identifier (OUI) to identify the vendor'

async def main(input_oui: str):
    """
    Main loop, returns are for tests only
    """
    try:
        cache = await aio_get_oui_cache(bypass=True)
        if not cache:
            record = await mac_lookup_call(input_oui)
            oui = record.get('macPrefix')
            vendor = record.get('company')
        else:
            record = cache.get_record(input_oui)
            oui = record.get('oui')
            vendor = record.get('vendor')
    except ValueError:
        print(f'MacTools: {input_oui} is not a valid MAC or OUI')
        return ValueError
    else:
        if record:
            oui = MacAddress.format_mac_address(oui, MacNotation.HYPHEN)
            print(f'{oui}: {vendor}')
            return vendor
        else:
            oui = MacAddress.format_mac_address(input_oui, MacNotation.HYPHEN)[:23]
            print(f'{oui}: No entries with IEEE')
            return None


async def handle_args():
    # Start the file IO first since it's the slowest task
    await create_pickle_task()

    parser = ArgumentParser(description='OUI CLI look-up')
    parser.add_argument('oui', type=str, help=help_str)
    args = parser.parse_args()
    await main(args.oui)

if __name__ == '__main__':
    run(handle_args())