# MacTools OUI Cache Setup

# Python Modules
from setuptools import setup, find_packages
from setuptools.command.install import install

# Local Modules
from mactools import __version__, update_ieee_files

# Custom Install Functions

class CustomInstall(install):
    def run(self):
        update_ieee_files(overwrite=True)
        install.run(self)

# Normal Install

DESCRIPTION = 'MAC Address-focused library similar to `ipaddress`'

with open('README.md', 'r', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='mactools',
    author='Michael Buckley',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    version=__version__,
    cmdclass={
        'install': CustomInstall,
    },
    packages=find_packages(),
    package_data={
        'mactools': ['resources/ieee/*.csv'],
    },
    keywords=['python','networking','network','mac','oui','ieee']
)