from argparse import ArgumentParser
from mactools import MacAddress, MacNotation, get_oui_cache

help_str = 'Organizationally Unique Identifier (OUI) to identify the vendor'

if __name__ == '__main__':
    parser = ArgumentParser(description='OUI CLI look-up')
    parser.add_argument('oui', type=str, help=help_str)
    args = parser.parse_args()
    try:
        record = get_oui_cache().get_record(args.oui)
    except ValueError:
        print(f'MacTools: {args.oui} is not a valid MAC or OUI')
    else:
        if record:
            oui, vendor = next(iter(record.items()))
            oui = MacAddress.format_mac_address(oui, MacNotation.HYPHEN)
            print(f'{oui}: {vendor}')
        else:
            oui = MacAddress.format_mac_address(args.oui, MacNotation.HYPHEN)[:23]
            print(f'{oui}: No entries with IEEE')
