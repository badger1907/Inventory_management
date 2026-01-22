

import hashlib


def hash_pass(password):
    password=str.encode(password)
    sha256=hashlib.sha256()
    sha256.update(password)
    e_password  = sha256.hexdigest()
    return e_password
