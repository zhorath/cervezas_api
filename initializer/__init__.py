"""
version: '1.0.0'
project: 'Cervezas API'
repo: '-'
author: 'richard.fernandez'
"""

# Import Python Methods
import os
import sys
import datetime

# Import Loggin Methods
import logging

# Set location variables
ABSFILEPATH = os.path.abspath(__file__)
FILEDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(FILEDIR)
ROOTTDIR = os.path.dirname(PARENTDIR)

# Import Project Path in Sys
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath(ROOTTDIR))
sys.path.append(os.path.abspath(PARENTDIR))
sys.path.append(os.path.abspath(FILEDIR))

# Get Debug Level
DEBUG_LEVEL_ENV = os.environ.get('DEBUG_LEVEL')
DEBUG = False

# Set Debug Level
if DEBUG_LEVEL_ENV == "0":
    DEBUG_LEVEL = logging.INFO
elif DEBUG_LEVEL_ENV == "1":
    DEBUG_LEVEL = logging.WARNING
elif DEBUG_LEVEL_ENV == "2":
    DEBUG_LEVEL = logging.DEBUG
    DEBUG = True
else:
    DEBUG_LEVEL = logging.INFO

# Check the logs directory
if not os.path.exists('logs'):

    # Create log folder
    os.makedirs('logs')

# Logging Init
logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(filename)s > l.#%(lineno)s | %(message)s',
    level=DEBUG_LEVEL,
    #filename=PARENTDIR + "/logs/app_log.log"
)

logging.debug("Reading __init__")

# Hard necessary dependencies
hard_dependencies = ('flask', 'yaml')
missing_dependencies = []

# Simple import to each dependency
for dependency in hard_dependencies:

    try:
        __import__(dependency)
    except ImportError as e:
        logging.error(f'Missing dependency: {dependency}')
        missing_dependencies.append(dependency)

# Check if all dependencies were imported successfully
if missing_dependencies:
    raise ImportError(f"Missing required dependencies {missing_dependencies}")

# Delete unnecessary variables
del hard_dependencies, dependency, missing_dependencies

# Import My Utilities
from utilities import redis_connect, sqlite_connect

# Import Yaml Methods
import yaml

# Open Config File
try:
    config_file = yaml.load(open('initializer/config.yml'), Loader=yaml.FullLoader)
except FileNotFoundError as e:
    logging.error('Config.yml is not found in the project path')
    sys.exit(0)

# Validations
if 'redis' not in config_file:
    raise NotImplementedError('redis config not found in the config_file')

# Validations
if 'app' not in config_file:
    raise NotImplementedError('app config not found in the config_file')

# Load Redis Config
logging.debug(f"Redis config: {config_file['redis']}")

# Connect with Redis
redis = redis_connect.Connect(**config_file['redis'])

# Export App
app_config = config_file['app']
app_config['debug'] = DEBUG

del config_file, yaml

__all__ = ['redis', 'app_config']
