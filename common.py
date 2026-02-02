

import hashlib


def hash_pass(password):
    password=str.encode(password)
    sha256=hashlib.sha256()
    sha256.update(password)
    e_password  = sha256.hexdigest()
    return e_password

def check_items(item, item_list):
    for i in item_list:
        if i._Record__product_code == item._Record__product_code:
            return True
    return False
