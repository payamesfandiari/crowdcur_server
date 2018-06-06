import os.path
from cubes.server import create_server,read_slicer_config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the configuration file name (and possibly whole path) here
CONFIG_PATH = os.path.join(CURRENT_DIR, "slicer3.ini")
config = read_slicer_config(CONFIG_PATH)
application = create_server(config)