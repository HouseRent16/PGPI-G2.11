import hashlib

def encoder_sha256(data):
    sha256 = hashlib.sha256()
    data_bytes = data.encode() if isinstance(data, str) else bytes(data)
    sha256.update(data_bytes)
    hash = sha256.hexdigest()
    return hash
