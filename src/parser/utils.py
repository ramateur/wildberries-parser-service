import hashlib


def generate_reproducible_id(data: str) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    hash_object = hashlib.sha256(data)

    return hash_object.hexdigest()
