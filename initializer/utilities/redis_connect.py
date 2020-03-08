# Import Python Libraries
import os

# Import Redis
import redis


def Connect(*args, **kwargs):
    """
    Connect to the database; see Connection.__init__() for more information.
    """
    return Connection(*args, **kwargs)


class Connection(object):
    """
    Representation of the connection with Redis.

    The proper way to get an instance of this class is to call connect().

    Establish a connection to the Redis database. Accepts several arguments:

    :param host: Host where the database server is located
    :param user: Username to log in
    :param database: Database to use, None to not use a particular one. (default: 0)
    :param port: Port to use, default is usually OK. (default: 6379)
    """
    __slots__ = ('host', 'database', 'port', 'conn', 'active_connection')

    def __init__(self, host: str=None, database: str=0, port: int=None):
        self.conn = None
        self.port = int(port) or 6379
        self.active_connection = False
        self.host = host or 'localhost'
        self.database = int(database) or 0

    def __enter__(self):
        # Connect to an existing database
        self._try_connection()
        return self.conn

    def _check_connection(self):
        if not self.active_connection:
            raise RuntimeError('No active connection to Redis')

    def _try_connection(self):
        # Manages TCP communication from a Redis server
        logging.debug('Attempt to connect to Redis')
        try:
            self.conn = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.database
            )
            logging.debug('Connected to Redis')
        except Exception as e:
            logging.error('Error, connecting to Redis')
            logging.error(e)
            raise Exception('Error, connecting to Redis')
        self.active_connection = True

    def connect(self):
        # Return raw connection without __enter__
        if self.conn is None:
            self._try_connection()
        return self.conn

    def __exit__(self, type, value, traceback):
        # Exiting to Redis
        logging.debug('Exiting to Redis')

        if self.active_connection:
            # Close communication with the database
            # Nothing to Do, Redis connection itself is closed
            pass
        self.active_connection = False
