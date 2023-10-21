# OUI IEEE TextFSM Template

OUI_TEMPLATE = """Value hex_oui ([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})
Value oui ([0-9A-F]{6})
Value vendor (.+)
Value street_address (.+)
Value city (.+)
Value state (\S+)
Value postal_code (.+)
Value country ([A-Z]{2})

Start
  ^${hex_oui}\s{3}\(hex\)\s{2}${vendor}
  ^${oui} -> GetStreetAddress

GetStreetAddress
  ^\s{4}${street_address} -> GetCity

GetCity
  ^\s{4}${city}\s{2,6}${state}\s{2,6}${postal_code} -> GetCountry
  ^\s{4}${city}\s{2,6}${postal_code} -> GetCountry

GetCountry
  ^\s{4}${country} -> Record Start"""