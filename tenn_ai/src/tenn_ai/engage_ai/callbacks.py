import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import yaml
import os

from tenn_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.utils.tenn_config_ai import TENN_ConfigAI
from tenn_ai.engage_ai.tenn_engage_ai import TENN_EngageAI

#########################################################################################################
# Callbacks
#########################################################################################################

def on_register_click(mainwindow: tk.Tk):
    username = mainwindow.root.root_middle_row.tabs_container.tab_welcome.tab_welcome_label.tab_welcome_username_input.get()
    password = mainwindow.root.root_middle_row.tabs_container.tab_welcome.tab_welcome_label.tab_welcome_password_input.get()
    msg = register(username, password)
    set_status(mainwindow, msg)

#########################################################################################################

def on_login_click(mainwindow: tk.Tk):
    username = mainwindow.root.root_middle_row.tabs_container.tab_welcome.tab_welcome_label.tab_welcome_username_input.get()
    password = mainwindow.root.root_middle_row.tabs_container.tab_welcome.tab_welcome_label.tab_welcome_password_input.get()
    msg = login(username, password)
    set_status(mainwindow, msg)

#########################################################################################################
# Support functions
#########################################################################################################

def set_status(mainwindow: tk.Tk, passed_status: str = ""):
    mainwindow.root.root_footer_row.footer_status_text.value = passed_status

#########################################################################################################

def load_credentials():
    properties = TENN_Properties()
    credentials_file = properties.login_credentials_path

    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            return yaml.safe_load(f)
    else:
        return {}

#########################################################################################################

def save_credentials(credentials):
    properties = TENN_Properties()
    credentials_file = properties.login_credentials_path

    with open(credentials_file, 'w') as f:
        yaml.dump(credentials, f)

#########################################################################################################

def register(username: str = "", password: str = ""):
    credentials = load_credentials()
    if username in credentials:
        return "Username already exists"
    credentials[username] = password
    save_credentials(credentials)
    return "Successfully registered"

#########################################################################################################

def login(username, password):
    credentials = load_credentials()
    if username in credentials and credentials[username] == password:
        return "Login successful"
    else:
        return "Invalid username or password"

"""
# Initialize Tkinter root
root = tk.Tk()
root.title("User Registration and Login")

# Create Username and Password fields
username_label = ttk.Label(root, text="Username:")
username_label.grid(column=0, row=0)
username_entry = ttk.Entry(root)
username_entry.grid(column=1, row=0)

password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=1)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(column=1, row=1)

# Register and Login buttons
register_button = ttk.Button(root, text="Register", command=on_register_click)
register_button.grid(column=0, row=2)
login_button = ttk.Button(root, text="Login", command=on_login_click)
login_button.grid(column=1, row=2)

# Status Label
status_label = ttk.Label(root, text="")
status_label.grid(columnspan=2, row=3)

root.mainloop()
"""