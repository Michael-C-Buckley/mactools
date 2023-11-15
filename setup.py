# MacTools OUI Cache Setup

from setuptools import setup, find_packages
from mactools.version import __version__

DESCRIPTION = 'MAC Address-focused library similar to `ipaddress`',

with open('README.md', 'r', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='MacTools',
    author='Michael Buckley',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'textfsm',
        'appdirs',
        'httpx'
    ],
    keywords=['python','networking','network','mac','oui','ieee']
)