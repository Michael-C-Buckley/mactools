from argparse import ArgumentParser
from mactools import MacAddress, MacNotation, get_oui_cache

help_str = 'Organizationally Unique Identifier (OUI) to identify the vendor'

def main(input_oui: str):
    """
    Main loop, returns are for tests only
    """
    try:
        record = get_oui_cache().get_record(input_oui)
    except ValueError:
        print(f'MacTools: {input_oui} is not a valid MAC or OUI')
        return ValueError
    else:
        if record:
            oui = MacAddress.format_mac_address(record.get('oui'), MacNotation.HYPHEN)
            vendor = record.get("vendor")
            print(f'{oui}: {vendor}')
            return vendor
        else:
            oui = MacAddress.format_mac_address(input_oui, MacNotation.HYPHEN)[:23]
            print(f'{oui}: No entries with IEEE')
            return None


def handle_args():
    parser = ArgumentParser(description='OUI CLI look-up')
    parser.add_argument('oui', type=str, help=help_str)
    args = parser.parse_args()
    main(args.oui)

if __name__ == '__main__':
    handle_args()