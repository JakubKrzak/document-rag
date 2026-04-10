import hashlib

def hash_file_content(file_content) -> str:
    return hashlib.sha256(file_content).hexdigest()