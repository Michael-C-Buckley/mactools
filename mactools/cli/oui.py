from argparse import ArgumentParser
from mactools import OUIRecord, MacAddress, MacNotation, get_oui_cache

help_str = 'Organizationally Unique Identifier (OUI) to identify the vendor'

if __name__ == '__main__':
    parser = ArgumentParser(description='OUI CLI look-up')
    parser.add_argument('oui', type=str, help=help_str)
    args = parser.parse_args()
    try:
        record: OUIRecord = get_oui_cache().get_record(args.oui)
    except ValueError:
        print(f'MacTools: {args.oui} is not a valid OUI')
    else:
        if record:
            oui = record.hex_oui
            if oui is None:
                oui = MacAddress.format_mac_address(args.oui, MacNotation.HYPHEN)[:8]
            print(f'{oui}: {record.vendor}')
        else:
            oui = MacAddress.format_mac_address(args.oui, MacNotation.HYPHEN)
            print(f'{oui}: No entries with IEEE')
