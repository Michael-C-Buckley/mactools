# MacTools OUI Cache Setup

# Python Modules
from asyncio import run, gather
from os import path, makedirs
from setuptools import setup, find_packages
from setuptools.command.install import install
from urllib.request import urlretrieve

# Local Modules
from mactools import __version__

# Custom Install Functions

async def get_csv_file(endpoint: str, dest_path: str) -> None:
    """"""
    url = f'https://standards-oui.ieee.org/{endpoint}.csv'
    filename = f'{dest_path}{endpoint.split("/")[1]}.csv'
    return urlretrieve(url, filename)

class CustomInstall(install):
    def run(self):
        install.run(self)
        print('MacTools: Fetching IEEE files...', end='\r')

        # Download IEEE files
        dest_path = path.join(self.install_lib, 'mactools/resources/ieee/')

        makedirs(dest_path, exist_ok=True)

        async def run_coroutines():
            tasks = [get_csv_file(i, dest_path) for i in ['oui/oui', 'oui28/mam', 'oui36/oui36']]
            return await gather(*tasks)

        results = run(run_coroutines())
        print('MacTools: IEEE Downloads completed...')

# Normal Install

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
    cmdclass={
        'install': CustomInstall,
    },
    packages=find_packages(),
    keywords=['python','networking','network','mac','oui','ieee']
)