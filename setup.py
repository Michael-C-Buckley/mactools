# OUI Cache Setup

from setuptools import setup, find_packages
from version import __version__

DESCRIPTION = 'MacTools',
LONG_DESCRIPTION = 'MAC Address-focused library similar to `ipaddress`'



setup(
    name='oui_cache',
    author='Michael Buckley',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'textfsm',
        'appdirs',
        'requests'
    ],
    keywords=['python','networking','network','mac','oui','ieee']
)