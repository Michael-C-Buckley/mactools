# Python Modules
from os import path as os_path
from sys import path as sys_path

# Third Party Modules
from appdirs import user_data_dir

# Add the project directory to sys.path
sys_path.append(os_path.dirname(os_path.dirname(os_path.dirname(os_path.abspath(__file__)))))

from version import __version__ as VERSION

# Cache file constants base, file will also include the Cache type
CACHE_DIR = user_data_dir('python3-mactools')
PICKLE_DIR = os_path.join(CACHE_DIR, 'oui.pkl')