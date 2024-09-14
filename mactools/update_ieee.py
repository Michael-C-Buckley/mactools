# MacTools IEEE Updater

# Python Modules
from asyncio import gather, run
from os import makedirs, path
from importlib.resources import files
from urllib.request import urlopen, Request

# Local Modules
from mactools.version import __version__

async def get_csv_file(endpoint: str, dest_path: str, overwrite: bool) -> None:
    """
    Coroutine for fetching individual CSV file from IEEE
    """
    filename = f'{path.join(dest_path, endpoint.split("/")[1])}.csv'
    if path.exists(filename) and not overwrite:
        return True
    url = f'https://standards-oui.ieee.org/{endpoint}.csv'
    filename = f'{path.join(dest_path, endpoint.split("/")[1])}.csv'

    headers = {
        'User-Agent': f'MacTools/{__version__} (https://github.com/Michael-C-Buckley/mactools)'
    }

    try:
        with urlopen(Request(url, headers=headers)) as response:
            if response.status == 200:
                with open(filename, 'wb') as file:
                    file.write(response.read())
                return True
    except Exception as e:
        pass

    return False

def update_ieee_files(overwrite: bool = True) -> bool:
    """
    Procedure for updating the IEEE CSV files within the project
    """
    print('MacTools: Fetching IEEE files...', end='\r')
    dest_path = files('mactools').joinpath('resources/ieee')

    makedirs(dest_path, exist_ok=True)

    async def run_coroutines():
        tasks = [get_csv_file(i, dest_path, overwrite) for i in ['oui/oui', 'oui28/mam', 'oui36/oui36']]
        return await gather(*tasks)

    results = run(run_coroutines())
    if False in results:
        print('MacTools: Error accessing IEEE, check your internet connection.')
        return False
    else:
        print('MacTools: IEEE Downloads completed...')
        return True

if __name__ == '__main__':
    update_ieee_files()