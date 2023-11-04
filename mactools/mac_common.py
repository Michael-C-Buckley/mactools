from typing import Union

def fill_hex(raw_input: Union[str, int], required_length: int):
    """
    Returns a hex string of `length` padded with leading zeros
    """
    case_dict = {
        int: lambda arg: hex(arg)[2:].upper(),
        str: lambda arg: arg.strip().upper()
    }
    case_func = case_dict.get(type(raw_input))
    prepared_input = case_func(raw_input)
    fill_length = int(required_length - len(prepared_input))
    filler_zeros = ''.zfill(fill_length)
    return f'{filler_zeros}{prepared_input}'

def hex_range(varying_chars: int, fixed_start: str = '', fixed_end: str = '',) -> str:
    """
    Returns a generator which iterates creates a range of hex.
    `fixed_start` and `fixed_end` are the leading and trailing fixed portions.
    `varying_chars` is the length of the hex string to be generated and filled.
    """
    for i in range(16**varying_chars):
        fill_part = fill_hex(i, varying_chars)
        yield f'{fixed_start}{fill_part}{fixed_end}'
