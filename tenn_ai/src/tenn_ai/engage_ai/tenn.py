#!/usr/bin/python3
import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk

from tenn_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.utils.tenn_config_ai import TENN_ConfigAI
from tenn_ai.engage_ai.tenn_engage_ai import TENN_EngageAI
import tenn_ai.engage_ai.callbacks as callbacks

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "tenn.ui"

class TennApp:
    def __init__(self, master=None):
        
        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.engageAI = TENN_EngageAI()

        # Create the builder
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("root", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def on_login_click(self):
        callbacks.on_login_click(self.mainwindow)

    def on_register_click(self):
        callbacks.on_register_click(self.mainwindow)

if __name__ == "__main__":
    app = TennApp()
    app.run()
