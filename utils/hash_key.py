import hashlib
import sys

def hash_key(key,salt=""):
    return hashlib.sha256(salt.encode() + key.encode()).hexdigest()

if __name__ == "__main__":
    key = sys.argv[1]
    salt = sys.argv[2]
    print(hash_key(key))