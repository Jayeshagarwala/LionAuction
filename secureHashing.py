import hashlib

def encode(string):
    encoded = hashlib.sha256(string.encode('UTF-8'))
    return encoded.hexdigest()
