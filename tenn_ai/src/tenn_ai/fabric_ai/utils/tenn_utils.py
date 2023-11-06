import os
import re
import hashlib
import uuid
from typing import List
import json

from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties

class TENN_Utils():

    def __init__(self, passed_verbose: bool = False):
        self.properties = TENN_Properties()
        self.verbose = passed_verbose

    ##############################################################################################################################
    # Function to return the file extension of a file

    def get_file_extension(self, passed_filepath: str) -> str:
        return os.path.splitext(passed_filepath)[-1].lower()

    ##############################################################################################################################
    # Function to return the full absolute path of a file or folder

    def get_full_path(self, passed_path: str) -> str:
        return os.path.abspath(passed_path)

    ##############################################################################################################################
    # Function to return the timestamp of a file

    def get_file_timestamp(self, passed_filepath: str) -> str:
        return os.path.getmtime(passed_filepath)

    ##############################################################################################################################
    # Function to clean a string and remove redundancies, to make it ready for edrakDB ingestion

    def clean_string(self, text : str):
        """
        This function takes in a string and performs a series of text cleaning operations. 

        Args:
            text (str): The text to be cleaned. This is expected to be a string.

        Returns:
            cleaned_text (str): The cleaned text after all the cleaning operations have been performed.
        """
        # Replacement of newline characters:
        text = text.replace('\n', ' ')
        
        # Stripping and reducing multiple spaces to single:
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # Removing backslashes:
        cleaned_text = cleaned_text.replace('\\', '')
        
        # Replacing hash characters:
        cleaned_text = cleaned_text.replace('#', ' ')
        
        # Eliminating consecutive non-alphanumeric characters:
        # This regex identifies consecutive non-alphanumeric characters (i.e., not a word character [a-zA-Z0-9_] and not a whitespace) in the string 
        # and replaces each group of such characters with a single occurrence of that character. 
        # For example, "!!! hello !!!" would become "! hello !".
        cleaned_text = re.sub(r'([^\w\s])\1*', r'\1', cleaned_text)
        
        return cleaned_text
    ############
    import re



    ##############################################################################################################################
    # Function to get a list of all files in a folder, and including files in subfolders recursively if the recursive flag is set to True

    def get_files_in_folder(self, passed_folder_path: str, passed_recursive: bool = False, passed_include_subfolder_paths: bool = False) -> list:

        # This function takes in a folder path and returns a list of all the files in that folder. If the recursive flag is set to True, 
        # then the function also returns files in all the subfolders of the passed folder path.

        # Get the list of all files in the folder

        paths = []

        if passed_recursive:
            # os.walk is used for recursive search
            for root, dirs, files in os.walk(passed_folder_path):
                if passed_include_subfolder_paths:
                    for dir in dirs:
                        paths.append(os.path.join(root, dir))
                for file in files:
                    paths.append(os.path.join(root, file))
        else:
            # os.listdir is used for non-recursive search
            for item in os.listdir(passed_folder_path):
                item_path = os.path.join(passed_folder_path, item)
                if os.path.isfile(item_path) or (passed_include_subfolder_paths and os.path.isdir(item_path)):
                    paths.append(item_path)

        return paths

    ##############################################################################################################################
    # Function to get all files in a folder

    def get_relevant_file_urls(self, passed_url: str, passed_recursive: bool = False) -> List[str]:
            
            # Get all the files in the folder
            # check if the file is not a folder and has an ignored extension
            
            urls = []

            # If the passed url is not a folder, then just add it to urls and return
            if not os.path.isdir(passed_url) and not self.has_ignored_extension(passed_url):
                urls.append(passed_url)
            else:
                # If the passed url is a folder, get all the files in the folder, based on the value of the recursive flag
                if self.verbose: print("TENN_Utils - get_relevant_urls() - Parsing: " + passed_url)
                all_files = self.get_files_in_folder(passed_folder_path = passed_url, passed_recursive = passed_recursive)
                
                # Add the files that don't have an ignored extension
                urls = [f for f in all_files if self.has_ignored_extension(f) == False]

            return urls

    ##############################################################################################################################

    # Function to check if a file has an extension in a specified list of ignored extensions

    def has_ignored_extension(self, passed_file_path: str) -> bool:
        # Set the properties and helpers
        properties = TENN_Properties()
            
        # Checks if a file has an extension in a specified list of extensions.
        # We should put this in a property file
        for extension in properties.ignored_extensions:
            if passed_file_path.lower().endswith(extension.lower()):
                return True
        return False

    ##############################################################################################################################

    # Function to hash a text based on sha256 protocol

    def hash_text(self, passed_text : str = ""):
        content = passed_text.encode('utf-8')
        hash_code = hashlib.sha256(content).hexdigest()
        return hash_code

    ##############################################################################################################################

    # Function to hash a file based on sha256 protocol

    def hash_file(self, passed_url : str = ""):
        """Generate SHA-256 hash for a file."""
        
        # Check if the passed_url is blank, is a valid url, and the file exists
        if passed_url == "" or not os.path.isfile(passed_url):
            if self.verbose: print("TENN_Utils - hash_file - The passed_url is blank, is not a valid url, or the file does not exist. Returning None.")  
            return None

        # Initialize a SHA-256 hasher
        sha256_hash = hashlib.sha256()

        # Open the file in binary read mode
        with open(passed_url, "rb") as f:
            # Read the file in chunks
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        # Return the hexadecimal representation of the hash
        return sha256_hash.hexdigest()

    ##############################################################################################################################
    
    # Function to generate a unique AID

    def generate_aid(self) -> str:
        return str(uuid.uuid4())
    
    ##############################################################################################################################

    # Function to convert a json object to html representation string

    def json_to_html(self, passed_json_data: json):
        # Convert the JSON object to a Python dictionary
        data = json.loads(passed_json_data)

        # Generate the HTML output
        html = "<ul>"
        for key, value in data.items():
            if isinstance(value, dict):
                html += f"<li>{key}: {self.json_to_html(json.dumps(value))}</li>"
            else:
                html += f"<li>{key}: {value}</li>"
        html += "</ul>"

        return html
    
    ##############################################################################################################################

    # Function to convert a string to html representation string

    def string_to_html(self, passed_string: str):
        # Generate the HTML output
        html = passed_string.replace("\n", "<br>")

        return html
    
    ##############################################################################################################################

    # Function to get collection name for a given content type

    def get_core_collection_name_for_content_type(self, passed_content_type: str):
        return self.properties.content_types_and_core_collection[passed_content_type]["core_collection"]
    
    ##############################################################################################################################

    # Function to get collection name for a given content type

    def get_core_awareness_type_for_content_type(self, passed_content_type: str):
        return self.properties.content_types_and_core_collection[passed_content_type]["core_awareness_type"]

    ##############################################################################################################################

    # Function to get embeddings model for a given content type

    def get_embeddings_model_for_collection(self, passed_collection: str):
        return self.properties.collections_and_embeddings_models[passed_collection]

    ##############################################################################################################################
    # Function to check if an email address is valid

    def is_valid_email(self, passed_email: str) -> bool:
        # Define a regular expression pattern for a valid email address
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Use the re module to match the pattern against the email address
        match = re.match(pattern, passed_email)
        # Return True if the email address matches the pattern, False otherwise
        return bool(match)
    
