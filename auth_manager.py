import hashlib
from crypto_manager import decrypt_folder

PASSWORD_HASH = "your_password_hash_here"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(password):

    if hash_password(password) == PASSWORD_HASH:

        decrypt_folder()
        print("Authentication successful")
        return True

    else:

        print("Authentication failed")
        return False