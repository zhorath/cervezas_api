# Import Wraps Methods
from functools import wraps

# Import Loggin Methods
import logging

# Import SQLite Mothods
import sqlite3

# Init Logging
logging.basicConfig(format='%(asctime)s -|- %(message)s')

logger = logging.getLogger('sqlite')
logger.addHandler(logging.FileHandler('logs/sqlite.log'))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)


def Connect(*args, **kwargs):
    """
    Connect to the database; see Connection.__init__() for more information.
    """
    return Connection(*args, **kwargs)


class Connection(object):
    """
    Representation of the connection with SQLite.

    The proper way to get an instance of this class is using "with" statement.

    Establish a connection to the SQLite database. Accepts several arguments:

    :param file: file name of the database
    """
    __slots__ = ('filedb', 'active_connection', 'conn', 'autocommit',
                 'check_same_thread', 'cursor', 'committed')

    def __init__(self, filedb: str, check_same_thread: bool=False, autocommit: bool=True):
        self.filedb = filedb
        self.autocommit = autocommit
        self.check_same_thread = check_same_thread
        self.active_connection = False
        self.conn = None
        self.cursor = None
        self.committed = False

    def __enter__(self):
        # Connect to an existing database
        self._try_connection()

        self.cursor = self.conn.cursor()
        return self.cursor

    def dict_factory(self, cursor, row):
        rows = {}
        for idx, col in enumerate(cursor.description):
            rows[col[0]] = row[idx]
        return rows

    def _try_connection(self):
        # Attempt to connect with SQLite
        logger.debug('Attempt to connect to SQLite')
        logger.debug(f'filedb: {self.filedb}')
        try:
            self.conn = sqlite3.connect(
                self.filedb,
                check_same_thread=self.check_same_thread
            )
            self.conn.row_factory = self.dict_factory
            logger.debug('Connected to SQLite')
        except psycopg2.Error as e:
            logger.error('Error, connecting to SQLite')
            logger.error(e)
            raise Exception('Error, connecting to SQLite')
        self.active_connection = True

    def connect(self):
        # Return raw connection without __enter__
        if self.conn is None:
            self._try_connection()
        return self.conn

    def __exit__(self, type, value, traceback):
        # Exiting to SQLite
        if not self.committed and self.autocommit:
            # Make the changes to the database persistent
            self.conn.commit()

        if self.active_connection:
            # Close communication with the database
            self.cursor.close()
            self.conn.close()
            self.active_connection = False
