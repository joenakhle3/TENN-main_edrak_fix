import os
import sys
import json
import datetime
import time
import uuid

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB

from sqlalchemy import Engine, Table, Column
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID, BLOB
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import chromadb
from chromadb.utils import embedding_functions

# Initialize the declarative base for sqlalchemy
Base = declarative_base()

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

# The Awareness class is the master record for any awareness that is create from any input
class TENN_Awareness(Base):

    # Define the table name in the database
    __tablename__ = 'awareness'

    # Define the table columns
    aid = Column(String(64), primary_key=True, unique=True, default=str(uuid.uuid4))
    url = Column(String(512), nullable=False, unique=True) # TODO change this later into a relationship with an Input object
    name = Column(String(64), nullable=True) # TODO we can use this to store a special name for the awareness from the user
    description = Column(String(256), nullable=True)
    input_type = Column(String(64), nullable=False) # FILE, URL, API, STREAM
    content_type = Column(String(64), nullable=False) # TEXT, DATA, CODE, JSON, IMAGE, VIDEO, AUDIO
    awareness_list = Column(Text, nullable=True) # this contains a JSON object with the list of all awareness created so far
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################

    # Define the constructor
    def __init__(self, passed_aid: str = "", passed_url: str = "", passed_name: str = "", passed_description: str = "", passed_input_type: str = "", passed_content_type: str = "", passed_awareness_list: str = ""):
        
        self.properties = TENN_Properties()

        # Set the passed variables
        self.aid = ""
        if passed_aid is not None and passed_aid != "": self.aid = passed_aid
        self.url = passed_url
        self.name = passed_name
        self.description = passed_description
        self.input_type = passed_input_type
        self.content_type = passed_content_type
        self.awareness_list = passed_awareness_list

    #########################################################################################################

    # Define the string representation of the object
    def __repr__(self):
        repr_string = "TENN_Awareness(" + \
                        "aid = " + str(self.aid) + ", " + \
                        "url = " + str(self.url) + ", " + \
                        "name = " + str(self.name) + ", " + \
                        "description = " + str(self.description) + ", " + \
                        "input_type = " + str(self.input_type) + ", " + \
                        "content_type = " + str(self.content_type) + ", " + \
                        "awareness_list = " + str(self.awareness_list) + ", " + \
                        "created = " + str(self.created) + ", " + \
                        "updated = " + str(self.updated) + ")"

        return repr_string                      

    #########################################################################################################

    # Add an awareness to the awareness list
    # The structure of the awareness list is 
    # [{"AWARENESS_TYPE": "TEXT.EXTRACTED_TEXT", "COLLECTION": "CORE_TEXT", "EMBEDDING_MODEL": "text-embedding-ada-002"},
    # {"AWARENESS_TYPE": "TEXT.GENERATED_SUMMARY", "COLLECTION": "GEN_SUMMARY", "EMBEDDING_MODEL": "text-embedding-ada-002"},
    # {"AWARENESS_TYPE": "TEXT.GENERATED_AUDIO", "COLLECTION": "GEN_AUDIO", "EMBEDDING_MODEL": "Whisper-0.1"}]

#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################

# Class that extends TENN_SqlDB to create all needed functions of the Edrak DB

# #########################################################################################################

class TENN_EdrakDB(TENN_SqlDB):
    
    #########################################################################################################

    # Initiatlize the class with the database type
    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        super().__init__(passed_db_path, passed_db_engine, passed_verbose)

    #########################################################################################################

    # Function to connect to the database
    def connect(self) -> Engine:
        # Create the engine based on db_type.
        self.engine = super().connect()
    
        # Create the tables, will be skipped if they already exist
        Base.metadata.create_all(self.engine)    
    
        # Return the engine
        return self.engine
    
    #########################################################################################################

    # Add a new awareness to the database
    # Returns the aid 
    def add_or_update_awareness(self, passed_awareness: TENN_Awareness = None) -> str:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - add_or_update_awareness - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed awareness is None
        if passed_awareness is None:
            if self.verbose: print("TENN_EdrakDB - add_or_update_awareness - The passed awareness is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        try:
            # Add the awareness to the database
            session.add(passed_awareness)
            session.commit()

            # Return the aid
            return passed_awareness.aid

        except:
            if self.verbose: print("TENN_EdrakDB - add_or_update_awareness - Error adding awareness to the database.")
            return None
        
        finally:
            session.close()


    #########################################################################################################

    # Function to get the awareness object by its aid

    def get_awareness(self, passed_aid : str = None) -> TENN_Awareness:
                
            # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - get_awareness - Not connected to the database. Connecting.")
            self.connect()
    
        # Check if the passed aid is None
        if passed_aid is None:
            if self.verbose: print("TENN_EdrakDB - get_awareness - The passed aid is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the awareness
        result_awareness = session.query(TENN_Awareness).filter(TENN_Awareness.aid == passed_aid).first()
        if self.verbose and result_awareness is not None: print("TENN_EdrakDB - get_awareness_for_url - Returned aid: " + str(result_awareness.aid))

        # Return the awareness
        return result_awareness


    #########################################################################################################

    # Function to get the awareness id for a URL in the database

    def get_awareness_for_url(self, passed_url : str = None) -> TENN_Awareness:

        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - get_awareness_for_url - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed url is None
        if passed_url is None:
            if self.verbose: print("TENN_EdrakDB - get_awareness_for_url - The passed url is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Check if the awareness exists
        result_awareness = session.query(TENN_Awareness).filter(TENN_Awareness.url == passed_url).first()
        if self.verbose and result_awareness is not None: print("TENN_EdrakDB - get_awareness_for_url - Returned aid: " + str(result_awareness.aid))

        # Return the awareness
        return result_awareness

    #########################################################################################################

    # Function to check if awareness exists for a URL in the database

    def awareness_exists_for_url(self, passed_url : str = None, passed_type: str = "") -> bool:
            
        # Check if the awareness exists
        if self.verbose: print("TENN_EdrakDB - awareness_exists_for_url - Checking if awareness exists for url: " + passed_url)
        result_aid = self.get_awareness_for_url(passed_url)

        # Return the awareness
        if result_aid is None:
            return False
        else:
            return True

    #########################################################################################################

    # Function to delete awareness by aid

    def delete_awareness(self, passed_aid : str = ""):
                
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - delete_awareness - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed aid is None
        if passed_aid is None or passed_aid == "":
            if self.verbose: print("TENN_EdrakDB - delete_awareness - The passed aid is None.")
            return None

        print ("TENN_EdrakDB - delete_awareness - Deleting awareness for aid: " + str(passed_aid))

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the awareness
        result_aid = session.query(TENN_Awareness).filter(TENN_Awareness.aid == passed_aid).first()

        # If the awareness exists, delete it
        if result_aid is not None:
            session.delete(result_aid)
            session.commit()
        else:
            if self.verbose: print("TENN_EdrakDB - delete_awareness - The awareness does not exist in the database. Skipping.")

    #########################################################################################################

    # Function to delete all awareness for a URL from the database

    def delete_awareness_for_url(self, passed_url : str = None):
            
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - delete_awareness_for_url - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed url is None
        if passed_url is None or passed_url == "":
            print("TENN_EdrakDB - delete_awareness_for_url - The passed url is empty.")
            return None

        if self.verbose: print ("TENN_EdrakDB - delete_awareness_for_url - Deleting awareness for url: " + passed_url)

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the awareness id
        result_aid = session.query(TENN_Awareness).filter(TENN_Awareness.url == passed_url).first()

        # If the awareness exists, delete it
        if result_aid is not None:
            session.delete(result_aid)
            session.commit()
        else:
            if self.verbose: print("TENN_EdrakDB - delete_awareness_for_url - The awareness does not exist in the database. Skipping.")
    
    #########################################################################################################

    # Function to return a list of all awareness in the database

    def get_all_awareness(self) -> list[TENN_Awareness]:
               
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_EdrakDB - get_all_awareness - Not connected to the database. Connecting.")
            self.connect()

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get all the awareness
        result_awareness_list = session.query(TENN_Awareness).all()

        # Return the awareness
        return result_awareness_list
 
    ###########################################################################################################################
    ##############################################################################################################################
    ##############################################################################################################################
    ##############################################################################################################################
    ##############################################################################################################################
    ##############################################################################################################################
    ##############################################################################################################################
    

    def get_edrakDB_collection(self, passed_type: str = "", passed_collection_name : str = None):
            
            # Let's set the knowledge type
            awareness_type = passed_type
            if (awareness_type == "") or (awareness_type is None) or (awareness_type.lower() not in self.properties.awareness_types):
                awareness_type = "text"

            # Infer the collection name from the type of knowledge
            if passed_collection_name is None:
                collection_name = self.properties.collection_name[awareness_type]
            else:
                collection_name = passed_collection_name.lower()
            
            # Infer the embedding function from the type of knowledge
            # WE NEED TO REVISIT THIS AND USE THE RIGHT EMBEDDING FUNCTIONS FOR EACH TYPE OF KNOWLEDGE, AND PREFERABLY USE LOCAL EMBEDDINGS ENGINES
            embedding_function_to_use = embedding_functions.OpenAIEmbeddingFunction(api_key = self.properties.openai_api_key, model_name = self.properties.embeddings_model[awareness_type] )

            # Get the collection based on the collection_name and embedding function
            return self.client.get_or_create_collection(name = collection_name, embedding_function = embedding_function_to_use)
    
    ##############################################################################################################################
    
    # Return the path to the edrakDB file for the passed path
    def get_edrakDB_path(self, passed_edrakdb_path : str = None):

        edrakDB_path = None

        # The options are:
        # 1- None, "" or . -> Use the current folder and append edrakDB
        if passed_edrakdb_path is None or passed_edrakdb_path == "" or passed_edrakdb_path == ".":
            edrakDB_path = os.path.join(os.getcwd(), self.properties.standard_edrak_db_path)

        # 2- A path that ends with edrakDB (whether it exists or not) -> Return it
        elif passed_edrakdb_path.endswith(self.properties.standard_edrak_db_path):
            edrakDB_path = passed_edrakdb_path

        # 3- A folder -> Create an edrakDB subfolder
        elif os.path.isdir(passed_edrakdb_path):
            edrakDB_path = os.path.join(passed_edrakdb_path, self.properties.standard_edrak_db_path)

        # 4- A file -> Create an edrakDB folder in the same folder (postponed for now)
        # elif os.path.isfile(passed_path):
        #    edrakDB_path = os.path.join(os.path.dirname(passed_path), TENN_Properties.standard_edrakDB_name)

        # for everything else, use the current folder and append edrakDB
        else: 
            edrakDB_path = os.path.join(os.getcwd(), self.properties.standard_edrak_db_path)
        
        return edrakDB_path