from typing import Union

from mactools.macaddress import MacAddress

def fill_hex(raw_input: Union[str, int], required_length: int, backfill: bool = False):
    """
    Returns a hex string of `length` padded with leading zeros
    """
    case_dict: dict[type, callable] = {
        int: lambda arg: hex(arg)[2:].upper(),
        str: lambda arg: arg.strip().upper()
    }
    case_func = case_dict.get(type(raw_input))
    prepared_input = case_func(raw_input)
    fill_length = int(required_length - len(prepared_input))
    filler_zeros = ''.zfill(fill_length)

    output_dict: dict[bool, str] = {
         False: f'{filler_zeros}{prepared_input}',
         True: f'{prepared_input}{filler_zeros}'
    }

    return output_dict.get(backfill)

def hex_range(varying_chars: int, fixed_start: str = '', fixed_end: str = '',) -> str:
    """
    Returns a generator which iterates creates a range of hex.
    `fixed_start` and `fixed_end` are the leading and trailing fixed portions.
    `varying_chars` is the length of the hex string to be generated and filled.
    """
    for i in range(16**varying_chars):
        fill_part = fill_hex(i, varying_chars)
        yield f'{fixed_start}{fill_part}{fixed_end}'

def prepare_oui(input_mac: Union[MacAddress, str]) -> str:
        """
        Takes a MAC or OUI and strips and prepares a unified clean OUI
        """
        if isinstance(input_mac, str):
            oui = MacAddress.clean_mac_address(input_mac)[0:6].upper()
        elif isinstance(input_mac, MacAddress):
            oui = input_mac.clean_oui
        return oui
