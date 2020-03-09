# Import json methods
import json

# Import Hashlib
import hashlib


def create_hash(data: object):
    if data is None:
        raise SyntaxError('Parameter data cannot be null')

    if isinstance(data, (str, int)):
        return hashlib.md5(
            data.encode('utf-8')
        ).hexdigest()

    if isinstance(data, (list, dict)):
        return hashlib.md5(
            json.dumps(data).encode('utf-8')
        ).hexdigest()

    raise SyntaxError('Data type cannot be hashed')
