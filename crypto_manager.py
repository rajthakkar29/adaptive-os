import os
import hashlib
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog

KEY_FILE = "secret.key"
PASSWORD_FILE = "master.hash"
TARGET_FOLDER = "secure_folder"


# ---------------- PASSWORD UI ----------------
def get_password_ui(prompt_text):

    root = tk.Tk()
    root.withdraw()

    # 🔥 FORCE TOP PRIORITY
    root.attributes("-topmost", True)
    root.lift()
    root.focus_force()

    # 🔥 BLOCK OTHER INTERACTIONS
    root.grab_set()

    password = simpledialog.askstring(
        "🔒 Security Alert",
        prompt_text,
        show="*",
        parent=root
    )

    root.grab_release()
    root.destroy()

    return password


# ---------------- SET PASSWORD ----------------
def set_master_password():

    password = get_password_ui("Set Master Password:")

    if not password:
        print("Password not set.")
        return

    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)

    print("Master password set.")


# ---------------- VERIFY PASSWORD ----------------
def verify_password():

    if not os.path.exists(PASSWORD_FILE):
        set_master_password()

    password = get_password_ui("Enter Master Password:")

    if not password:
        return False

    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    with open(PASSWORD_FILE, "r") as f:
        stored_hash = f.read()

    return hashed_input == stored_hash


# ---------------- KEY MANAGEMENT ----------------
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()


# ---------------- ENCRYPT / DECRYPT ----------------
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


# ---------------- LOCK FOLDER ----------------
def lock_folder():

    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(TARGET_FOLDER):

        file_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(file_path):
            encrypt_file(file_path, fernet)

    print("Folder Locked")


# ---------------- UNLOCK FOLDER ----------------
def unlock_folder():

    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(TARGET_FOLDER):

        file_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(file_path):
            decrypt_file(file_path, fernet)

    print("Folder Unlocked")


# ---------------- CHECK LOCK STATE ----------------
def is_folder_unlocked():

    try:
        for filename in os.listdir(TARGET_FOLDER):

            file_path = os.path.join(TARGET_FOLDER, filename)

            with open(file_path, "rb") as f:
                data = f.read(50)

            if b"gAAAA" in data:  # Fernet signature
                return False

        return True

    except:
        return False


# ---------------- RED TIER UNLOCK ----------------
def red_tier_unlock():

    print("High Risk Detected")

    if verify_password():
        unlock_folder()
        print("Access granted.")
        return True
    else:
        print("Incorrect password.")
        return False