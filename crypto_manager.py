import os
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass

KEY_FILE = "secret.key"
PASSWORD_FILE = "master.hash"
TARGET_FOLDER = "secure_folder"


def set_master_password():
    password = getpass("Set master password: ")
    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)

    print("Master password set.")


def verify_password():

    if not os.path.exists(PASSWORD_FILE):
        set_master_password()

    password = getpass("Enter master password: ")
    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    stored_hash = open(PASSWORD_FILE, "r").read()

    return hashed_input == stored_hash


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():

    if not os.path.exists(KEY_FILE):
        generate_key()

    return open(KEY_FILE, "rb").read()


def encrypt_file(file_path, fernet):

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(file_path, "wb") as f:
        f.write(encrypted)


def decrypt_file(file_path, fernet):

    with open(file_path, "rb") as f:
        data = f.read()

    try:
        decrypted = fernet.decrypt(data)

        with open(file_path, "wb") as f:
            f.write(decrypted)

    except:
        pass


def lock_folder():

    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(TARGET_FOLDER):

        file_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(file_path):
            encrypt_file(file_path, fernet)

    print("Folder Locked")


def unlock_folder():

    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(TARGET_FOLDER):

        file_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(file_path):
            decrypt_file(file_path, fernet)

    print("Folder Unlocked")


def red_tier_unlock():

    print("High Risk Detected")

    if verify_password():

        unlock_folder()
        print("Access granted. Folder will remain unlocked.")
        return True

    else:

        print("Incorrect password.")
        return False