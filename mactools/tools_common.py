# MacTool Common Resources File

from re import search, compile as re_compile

HEX_PATTERN = r'[a-fA-F0-9]'
HEX_PAIR = f'{HEX_PATTERN}{{2}}'
MAC_PORTION = fr'{HEX_PAIR}[:\-\. ]?'
HEX_REGEX = re_compile(HEX_PATTERN)

EUI48_PATTERN = f'(?:{MAC_PORTION}){{5}}{HEX_PAIR}'
EUI64_PATTERN = f'(?:{MAC_PORTION}){{7}}{HEX_PAIR}'
MAC_PATTERN = f'{EUI48_PATTERN}|{EUI64_PATTERN}'

EUI48_REGEX = re_compile(EUI48_PATTERN)
EUI64_REGEX = re_compile(EUI64_PATTERN)
MAC_REGEX = re_compile(MAC_PATTERN)

OUI_PATTERN = f'(?:{MAC_PORTION}){{2}}{HEX_PAIR}'
OUI28_PATTERN = f'(?:{MAC_PORTION}){{3}}{HEX_PATTERN}'
OUI36_PATTERN = f'(?:{MAC_PORTION}){{4}}{HEX_PATTERN}'

OUI_REGEX = re_compile(OUI_PATTERN)
OUI28_REGEX = re_compile(OUI28_PATTERN)
OUI36_REGEX = re_compile(OUI36_PATTERN)

def get_hex_value(hex_string: str) -> int:
    """
    Returns the bit value of a hex string or -1 for invalid strings
    """
    bit_value = 0
    for char in hex_string:
        if (match := search(r'([0-9a-fA-F])?([ \-\.:])?', char)):
            if match.group(1):
                bit_value += 4
            elif match.group(2):
                continue
            else:
                return -1
        
    return bit_value
