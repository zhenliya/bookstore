from hashlib import sha256

def get_hash(str):
    sh = sha256()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()

