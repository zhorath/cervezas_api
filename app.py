# Import OS Library
import os

# Import Initializer Module
from initializer import *

# Import App
from routes.settings import app


if __name__ == '__main__':
    app.run(
        host=app_config['host'],
        port=app_config['port'],
        debug=app_config['debug']
    )
