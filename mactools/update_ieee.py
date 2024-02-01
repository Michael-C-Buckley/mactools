# MacTools IEEE Updater

# Python Modules
from asyncio import gather, run
from os import makedirs, path
from pkg_resources import resource_filename
from urllib.request import urlretrieve

async def get_csv_file(endpoint: str, dest_path: str) -> None:
    """
    Coroutine for fetching individual CSV file from IEEE
    """
    url = f'https://standards-oui.ieee.org/{endpoint}.csv'
    filename = f'{path.join(dest_path, endpoint.split("/")[1])}.csv'
    try:
        urlretrieve(url, filename)
    except:
        return False
    else:
        return True

def update_ieee_files() -> bool:
    """
    Procedure for updating the IEEE CSV files within the project
    """
    print('MacTools: Fetching IEEE files...', end='\r')
    dest_path = resource_filename('mactools', 'resources/ieee')

    makedirs(dest_path, exist_ok=True)

    async def run_coroutines():
        tasks = [get_csv_file(i, dest_path) for i in ['oui/oui', 'oui28/mam', 'oui36/oui36']]
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