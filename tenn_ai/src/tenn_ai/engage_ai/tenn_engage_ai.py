# class to interact with the ui

import sys
import os
import json
import datetime
import time
import uuid

from tenn_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.utils.tenn_config_ai import TENN_ConfigAI
from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db import TENN_EdrakDB

#########################################################################################################

class TENN_EngageAI():

    def __init__(self):

        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        # Get the configAI object
        self.configAI = TENN_ConfigAI()
        self.populate_configAI_from_UI()
        
        # If the passed path is a folder, use it as the path, otherwise get the edrakDB path for the passed path
        self.edrakdb_path = self.configAI.get_edrakDB_path()
        print ("TENN_OrganizeAI - Loaded awareness DB with path " + self.edrakdb_path)

    #####################################################################################################

    def populate_configAI_from_UI(self):
        # TODO - Populate the configAI object from the UI
        return

    #####################################################################################################

    def login(self):
        # TODO - Call an API to login
        return "loggedin_username"
    
    #####################################################################################################

    def logout(self):
        # TODO - Call an API to logout
        return

    #####################################################################################################

    def get_aids(self):
        # TODO - Call an API to get the aids from edrakDB
        edrakDB = TENN_EdrakDB(self.edrakdb_path)
        client = edrakDB.get_edrakDB_client()
        collection = edrakDB.get_edrakDB_collection(passed_awareness_type = "text")
        return # collection.get_all_aids()
    