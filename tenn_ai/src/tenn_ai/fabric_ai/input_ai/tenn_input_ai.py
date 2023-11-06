# TENN_InputAI is the controller class for all input activities.
# It is responsible for receiving inputs (Documents, URLs, APIs, Streams) and using the TENN_Ingest class to ingest them
# It uses an ingest_input() function to process any input that comes in
# It uses TENN_Ingest to extract the URL contents and hashcode from each input
# Then it invokes TENN_EdrakAI to create_awareness() for each input, passes the URL, contents and chunks, and returns the awareness ID (AID)

import os
import glob
import sys
import argparse
import time
from urllib.parse import urlparse

# # Set the logging level for SQLAlchemy to a higher level to hide INFO messages.
# logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.edrak.databases.tenn_input_db import TENN_InputDB, TENN_Input, TENN_Input_Contents
from tenn_ai.fabric_ai.input_ai.tenn_ingest import TENN_Ingest
from tenn_ai.fabric_ai.edrak.tenn_edrak_ai import TENN_EdrakAI
from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db import TENN_Awareness

from fastapi import APIRouter, HTTPException
from typing import Optional, List, Union, Dict
from datetime import datetime
from pydantic import BaseModel
# ##############################################################################################################################

# Class to handle all input activities

class TENN_InputAI:

    # Constructor
    def __init__(self, passed_verbose: bool = False):

        # Set the properties and helpers
        self.properties= TENN_Properties()

        self.utils = TENN_Utils()
        self.verbose: bool = passed_verbose

        # Set the needed variables
        self.inputDB = TENN_InputDB(self.verbose)
        self.edrakAI = TENN_EdrakAI(self.verbose)
    

        # Connect to the input DB
        self.engine = self.inputDB.connect()


    ##############################################################################################################################

    # Function to process a list of input URLs

    def process_inputs(self, passed_url_list: list = [], passed_url_type = "FILE", passed_force_creation: bool = False) -> list:

        
        # Check if passed_url_list is empty or None and return an error
        if passed_url_list is None or passed_url_list == []:
            if self.verbose: print("TENN_InputAI - ingest_inputs - Error: Please specify a list of URLs.")
            return None

        # If the URL type is empty or not in our list of input types, return an error
        if passed_url_type is None or passed_url_type == "" or passed_url_type not in self.properties.input_types:
            if self.verbose: print("TENN_InputAI - ingest_input - Error: Please specify a valid URL type.")
            return None

        for url in passed_url_list:
            if (passed_url_type == "FILE"):
                self.process_input_file(url)

            elif (passed_url_type == "URL"):
                
                self.process_input_url(url)
            
            # TODO Add handlers for API and STREAM

    ##############################################################################################################################

    # Function to ingest an input by URL, of type FILE
    # It receives the URL and uses the TENN_Ingest class to ingest it
    # It then calls the TENN_EdrakAI to create awareness for the URL, contents and chunks

    def process_input_file(self, passed_url: str = "") -> TENN_Input:
            
        # If the URL is empty, return an error
        if passed_url is None or passed_url == "":
            if self.verbose: print("TENN_InputAI - process_input_file - Error: Please specify a URL.")
            return None

        # Get the Hashcode for the url file
        hashcode = self.utils.hash_file(passed_url)

        # Check if the hashcode exists in the inputDB
        if self.inputDB.input_exists_for_hashcode(hashcode):
            if self.verbose: print("TENN_InputAI - process_input_file - Found the Hashcode in the database, returning that Input.")
            return self.inputDB.get_input_by_hashcode(hashcode)
        

        # Here we are sure the Hashcode does not exist, therefore the content is new or modified
        # Read the file contents through a multimodal adapter
        ingest = TENN_Ingest(passed_url=passed_url, passed_url_type="FILE", passed_verbose=self.verbose)
        
        input_contents: TENN_Input_Contents = ingest.read_url_contents()
   

        # Create a new Input object
        final_input = TENN_Input(
                                passed_aid='none',
                                passed_url=passed_url,
                                passed_input_type='Text',
                                passed_hashcode=hashcode,)

        # Check if the URL exists in the inputDB
        existing_input: TENN_Input = self.inputDB.get_input_by_url(passed_url)

        # If it exists, that means the contents have changed
        if existing_input is None: # The URL does not exist in our InputDB
            if self.verbose: print("TENN_InputAI - process_input_file - Creating the input.")
            # Create a new Input object
            # With new Input ID, URL, Type
            # Update Hashcode, Timestamp
            # final_input = TENN_Input()
            final_input.url = passed_url
            final_input.input_type = "FILE"
            final_input.hashcode = hashcode


        else: # We have an existing URL, but the contents have changed
            if self.verbose: print("TENN_InputAI - process_input_file - The URL already exists in the database, updating the input.")

            # Keep Input ID, AID, URL, Input Type, but change the hashcode
            final_input = existing_input
            final_input.hashcode = hashcode

        # Store the Input object in the database and get its input ID
        final_input.input_id = self.inputDB.create_or_update_input(passed_input = final_input)
        
        # Create awareness
        final_awareness: TENN_Awareness = self.edrakAI.create_or_update_core_awareness(passed_input = final_input, passed_input_contents = input_contents)
        
        # Store the Input object again to update the generated aid
        final_input.aid = final_awareness.aid
        final_input.input_id = self.inputDB.create_or_update_input(passed_input = final_input)

        return final_input

    ##############################################################################################################################

    # Function to ingest an input by URL, of type URL
    # It receives the URL and uses the TENN_Ingest class to ingest it
    # It then calls the TENN_EdrakAI to create awareness for the URL, contents and chunks

    def process_input_url(self, passed_url: str = "") -> TENN_Input:

        # If the URL is empty, return an error
        if passed_url is None or passed_url == "":
            if self.verbose: print("TENN_InputAI - process_input_url - Error: Please specify a URL.")
            return None

        # Read the URL contents through a multimodal adapter
        ingest = TENN_Ingest(passed_url, "URL")
        input_contents: TENN_Input_Contents = ingest.read_url_contents()

        # Get the Hashcode for the url file
        hashcode = self.utils.hash_text(input_contents.full_content) 
        
        # Check if the hashcode exists in the inputDB
        if self.inputDB.input_exists_for_hashcode(hashcode):
            if self.verbose: print("TENN_InputAI - process_input_url - Found the Hashcode in the database, returning that Input.")
            return self.inputDB.get_input_by_hashcode(hashcode)

        # Create a new Input object
        final_input = TENN_Input()

        # Check if the URL exists in the inputDB
        existing_input: TENN_Input = self.inputDB.get_input_by_url(passed_url)

        # If it exists, that means the contents have changed
        if existing_input is None: # The URL does not exist in our InputDB
            if self.verbose: print("TENN_InputAI - process_input_url - Creating the input.")
            # Create a new Input object
            # With new Input ID, URL, Type
            # Update Hashcode, Timestamp
            final_input = TENN_Input()
            final_input.url = passed_url
            final_input.input_type = "URL"
            final_input.hashcode = hashcode

        else: # We have an existing URL, but the contents have changed
            if self.verbose: print("TENN_InputAI - process_input_url - The URL already exists in the database, updating the input.")

            # Keep Input ID, AID, URL, Input Type, but change the hashcode
            final_input = existing_input
            final_input.hashcode = hashcode

        # Store the Input object in the database and get its input ID
        final_input.input_id = self.inputDB.create_or_update_input(passed_input = final_input)

        # Create awareness
        final_input.aid = self.edrakAI.create_or_update_core_awareness(passed_input = final_input, passed_input_contents = input_contents)

        # Store the Input object again to update the generated aid
        final_input.input_id = self.inputDB.create_or_update_input(passed_input = final_input)

        return final_input
    
