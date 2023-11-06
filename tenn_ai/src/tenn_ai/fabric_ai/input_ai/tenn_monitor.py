import os
import time
import sys
from typing import List

from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.input_ai.tenn_input_ai import TENN_InputAI

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

##################################################################################################################

# Class TENN_Monitor takes a folder and starts monitoring it for changes

class TENN_Monitor():

    # Constructor

    def __init__(self, passed_folder: str = "", passed_verbose: bool = False):
        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.inputAI = TENN_InputAI()
        self.verbose = passed_verbose
        self.folder = None

        # Check if the passed folder is valid
        if passed_folder is None or passed_folder == "" or not os.path.isdir(passed_folder):
            if self.verbose: print("TENN_Monitor - Error: Please provide a valid folder.")
            return None
        else:
            self.folder = passed_folder


    #######################################################################################
    # Function to start monitoring a folder for file changes.

    def start_monitoring(self): 

        # Create an instance of FileChangeHandler
        event_handler = FileChangeHandler(self.folder)
    
        """Starts monitoring a folder for file changes."""

        # Generate inputs for the entire folder when initializing, without forcing generation
        print("InputAI TENN_Monitor - Refreshing inputs at startup for the folder: " + self.folder)

        # Get all the relevant urls and ask inputAI to ingest them (this is a refresh)
        urls = self.utils.get_relevant_file_urls(self.folder, passed_recursive=True)
        print(urls)
        self.inputAI.process_inputs(passed_url_list = urls, passed_force_creation=False)

        # Start monitoring the folder
        print("EdrakFS TENN_Monitor - Starting monitoring of folder: " + self.folder)
        observer = Observer()
        observer.schedule(event_handler, self.folder, recursive=True)
        observer.start()
        print("EdrakFS TENN_Monitor - Monitoring started.")
        
        try:
            while True: # add condition here
                time.sleep(1) 
                # define interrupt function here
                # function needs to be invoked from UI

        # TODO Add an interrupt from the UI to stop monitoring

        except KeyboardInterrupt:
            print("EdrakFS TENN_Monitor - Monitoring stopped.")
            observer.stop()
        observer.join()

##################################################################################################################

# Class to handle file system events.

class FileChangeHandler(FileSystemEventHandler):
    # Constructor
    
    ##############################################################################################
    def __init__(self, passed_folder: str = "", passed_verbose: bool = False):
        super().__init__()
        """Initialize the handler."""
        self.monitored_folder = passed_folder
        self.utils = TENN_Utils()
        self.inputAI = TENN_InputAI()
        self.properties = TENN_Properties()
        self.verbose = passed_verbose

    ##############################################################################################
    # Called when a file or folder is created.
    def on_created(self, event):

        # if the event.src_path is a folder, we don't want to do anything
        if os.path.isdir(event.src_path) or self.utils.has_ignored_extension(event.src_path):
            return

        if self.verbose: print("\n\nTENN_Monitor - Processing created file: " + event.src_path)
        self.inputAI.process_inputs(passed_url_list = [event.src_path], passed_url_type = "FILE", passed_force_creation=False)

    ##############################################################################################
    # Called when a file or folder is modified.
    def on_modified(self, event):

        # if the event.src_path is a folder, we don't want to do anything
        if os.path.isdir(event.src_path) or self.utils.has_ignored_extension(event.src_path):
            return

        if self.verbose: print("\n\nTENN_Monitor - Processing modified file: " + event.src_path)
        self.inputAI.process_inputs(passed_url_list = [event.src_path], passed_url_type = "FILE", passed_force_creation=False)

    ##############################################################################################
    # Called when a file or folder is moved.
    def on_moved(self, event):
        # if the event.src_path is a folder, we don't want to do anything
        if os.path.isdir(event.dest_path) or self.utils.has_ignored_extension(event.dest_path):
            return

        if self.verbose: print("\n\nTENN_Monitor - Processing moved file")
        if self.verbose: print("\nFrom: " + event.src_path)
        if self.verbose: print("\nTo: " + event.dest_path)
        self.inputAI.delete_inputs(passed_url_list = [event.src_path], passed_url_type = "FILE")
        self.inputAI.process_inputs(passed_url_list = [event.dest_path], passed_url_type = "FILE", passed_force_creation=False)

    ##############################################################################################
    # Called when a file or folder is deleted.
    def on_deleted(self, event):

        # if the event.src_path is a folder, we don't want to do anything
        if os.path.isdir(event.src_path) or self.utils.has_ignored_extension(event.src_path):
            return

        if self.verbose: print("\n\nTENN_Monitor - Processing deleted file: " + event.src_path)
        self.inputAI.delete_inputs(passed_url_list = [event.src_path], passed_url_type = "FILE")

