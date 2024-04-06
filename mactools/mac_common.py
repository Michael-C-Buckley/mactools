# MacTools Common Module

# Python Modules
from random import randint
from typing import Union
from typing import Iterator

# Local Modules
from mactools.basemac import BaseMac, MacNotation

def fill_hex(raw_input: Union[str, int], required_length: int, backfill: bool = False) -> str:
    """
    Returns a hex string of `length` padded with leading zeros
    """
    case_dict: dict[type, callable] = {
        int: lambda arg: hex(arg)[2:].upper(),
        str: lambda arg: str(arg).strip().upper()
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

def hex_range(varying_chars: int, fixed_start: str = '', fixed_end: str = '') -> Iterator[str]:
    """
    Returns a generator which iterates creates a range of hex.
    `fixed_start` and `fixed_end` are the leading and trailing fixed portions.
    `varying_chars` is the length of the hex string to be generated and filled.
    """
    for i in range(16**varying_chars):
        fill_part = fill_hex(i, varying_chars)
        yield f'{fixed_start}{fill_part}{fixed_end}'

def prepare_oui(input_mac: Union[BaseMac, str, int], full: bool = True) -> str:
        """
        Takes a MAC or OUI and strips and prepares a unified clean OUI
        """
        lookup_key = BaseMac if isinstance(input_mac, BaseMac) else type(input_mac)
        mac = {
            str: lambda: BaseMac.clean_mac_address(input_mac),
            int: lambda: BaseMac.number_to_hex_mac(input_mac, MacNotation.CLEAN),
            BaseMac: lambda: input_mac.clean,
        }.get(lookup_key)()

        return mac if full and mac else mac[:6]

# Create Random MAC or Hex

def create_random_hex_bit() -> str:
    """
    Returns a single bit between 0-9 or A-F
    """
    return hex(randint(0, 15))[2:3].upper()

def create_random_hex_string(length: int = 2) -> str:
    """
    Returns a hex string of specified length
    """
    bit_list = [create_random_hex_bit() for _ in range(length)]
    return ''.join(bit_list)

def create_random_mac(eui: int = 48, delimiter: MacNotation = MacNotation.COLON) -> str:
    """
    Returns a valid random MAC address
    """
    eui = int(eui)
    if eui not in [48, 64]:
        raise ValueError('EUI must be either `48` or `64`')

    hex_length = 4 if delimiter == MacNotation.PERIOD else 2
    segments = eui/(4*hex_length)
    
    mac_portions = [create_random_hex_string(hex_length) for _ in range(int(segments))]
    return delimiter.value.join(mac_portions)