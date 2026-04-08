import os
import hashlib
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, messagebox

KEY_FILE = "secret.key"
PASSWORD_FILE = "master.hash"
TARGET_FOLDER = "secure_folder"


# ---------------- UI INPUT ----------------
def get_password_input(prompt):

    root = tk.Tk()
    root.attributes("-topmost", True)  
    root.withdraw()

    password = simpledialog.askstring(
        "Authentication",
        prompt,
        show="*",
        parent=root
    )

    root.destroy()
    return password


# ---------------- PASSWORD ----------------
def set_master_password():

    password = get_password_input("Set master password:")

    if not password:
        return

    hashed = hashlib.sha256(password.encode()).hexdigest()

    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)

    messagebox.showinfo("Success", "Master password set.")


def verify_password():

    if not os.path.exists(PASSWORD_FILE):
        set_master_password()

    password = get_password_input("Enter master password:")

    if password is None:
        return False

    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    stored_hash = open(PASSWORD_FILE, "r").read()

    return hashed_input == stored_hash


# ---------------- KEY ----------------
def generate_key():

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():

    if not os.path.exists(KEY_FILE):
        generate_key()

    return open(KEY_FILE, "rb").read()


# ---------------- ENCRYPTION ----------------
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


# ---------------- FOLDER ----------------
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


# ---------------- RED TIER ----------------
def red_tier_unlock():

    if verify_password():

        unlock_folder()
        messagebox.showinfo("Access Granted", "Folder unlocked")

        return True

    else:

        messagebox.showerror("Access Denied", "Incorrect password")

        return False