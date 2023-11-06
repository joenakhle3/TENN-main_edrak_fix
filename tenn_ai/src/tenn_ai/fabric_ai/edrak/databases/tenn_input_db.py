import os
import sys
import json

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties 
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils 
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB

# Import SQLalchemy
from sqlalchemy import Engine, Table, Column, String, Integer, Sequence
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey,Index
from sqlalchemy.orm import mapper, sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func

# Initialize the declarative base for sqlalchemy
Base = declarative_base()

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################


# ####################################################################################
class TENN_Input(Base):

    # Define the table name in the database
    __tablename__ = 'inputs'
    # ForeignKey('awareness.aid'),

    input_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    aid = Column(String(64),  nullable=True, unique=True)
    url = Column(String(512), nullable=False, unique=True) 
    input_type = Column(String(64), nullable=False) # FILE, URL, API, STREAM
    hashcode = Column(String(256), nullable=False, unique=True)
    timestamp = Column(DateTime, default=func.now())

    # Define the constructor
    def __init__(self, passed_aid: str, passed_url: str, passed_input_type: str, passed_hashcode: str):
        self.aid = passed_aid
        self.url = passed_url
        self.input_type = passed_input_type
        self.hashcode = passed_hashcode
        # self.timestamp = passed_timestamp

    # Define the string representation of the object
    def __repr__(self):
        return "<TENN_Input(input_id='{}', aid='{}', url='{}', input_type='{}', hashcode='{}', timestamp='{}')>".format(
    self.input_id, self.aid, self.url, self.input_type, self.hashcode, self.timestamp)

    # Define the get and set functions for all properties of the object
    def get_input_id(self):
        return self.input_id

    def set_input_id(self, value):
        self.input_id = value

    def get_aid(self):
        return self.aid

    def set_aid(self, value):
        self.aid = value

    def get_url(self):
        return self.url

    def set_url(self, value):
        self.url = value

    def get_input_type(self):
        return self.input_type

    def set_input_type(self, value):
        self.input_type = value

    def get_hashcode(self):
        return self.hashcode

    def set_hashcode(self, value):
        self.hashcode = value

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, value):
        self.timestamp = value

# ##############################################################################################################################

# Class to handle all input contents and structure

# What chroma expects
# When you add this object, the embeddings are added automatically by chromadb based on the set embeddings model

# documents=["doc1", "doc2", "doc3", ...],
# embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
# metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
# ids=["id1", "id2", "id3", ...]
# distances=[[0.0, 0.1, 0.2], [0.1, 0.0, 0.3], [0.2, 0.3, 0.0], ...] (Optional)

class TENN_Input_Contents:

    # Constructor
    def __init__(self, passed_verbose: bool = False):
        self.verbose = passed_verbose
        self.full_content = None # Could be a string or a binary 
        self.url = "" # str
        self.input_type = "" # str could be FILE, URL, API, STREAM
        self.content_type = "" # str could be TEXT, IMAGE, VIDEO, AUDIO, JSON, BINARY
        self.documents = None # List of chunks, string or binary ["chunk1",         "chunk2", ...]
        # self.embeddings = None # List of lists of embeddings     [[1.1, 2.3, 3.2],  [4.5, 6.9, 4.4], ...] automatically added
        self.ids = None # List of chunk ids                      ["id1",            "id2", ...]
        self.metadatas = None # List of dict of tuples           [{"key": "value", "key": "value"}, {"key": "value", "key": "value"}, ...]
    


#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################

##############################################################################################################################

# Class that handles all Input DB activities

class TENN_InputDB(TENN_SqlDB):

    ##################################################################################
    # Initiatlize the class with the database type
    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):
        super().__init__(passed_db_path=passed_db_path, passed_db_engine=passed_db_engine, passed_verbose=passed_verbose)

        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.database_path = passed_db_path

    ##################################################################################
    # Function to connect to the database
    def connect(self) -> Engine:
        # Create the engine based on db_type.
        self.engine = super().connect()
    
        # Create the tables, will be skipped if they already exist
        Base.metadata.create_all(self.engine)    
    
        # Return the engine
        return self.engine
        
    ##################################################################################
    def search_by_hashcode(self, hashcode):

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Use the session to execute database queries
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            result = session.query(TENN_Input).filter_by(hashcode=hashcode).first()
            # Process the query result here
            return result
        finally:
            session.close()  # Make sure to close the session when done

    #########################################################################################################

    # Add a new input to the database
    def create_or_update_input(self, passed_input: TENN_Input = None) -> int:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()

        # Check if the passed input is None
        if passed_input is None:
            if self.verbose: print("TENN_InputDB - add_or_update_input - The passed input is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        try:
            # Add the input to the database
            session.add(passed_input)
            session.commit()

            # Return the aid
            return passed_input.input_id
        
        except:
            if self.verbose: print("TENN_InputDB - add_or_update_input - Error adding input to the database.")
            return None
        finally:
            session.close()  # Make sure to close the session when done

    #########################################################################################################

    # Function to get the input object for an input id in the database

    def get_input_by_id(self, passed_id : int = 0) -> TENN_Input:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()

        # Check if the passed url is None
        if passed_id is None or passed_id == 0:
            if self.verbose: print("TENN_InputDB - get_input_by_id - The passed id is invalid.")
            return None

        try:
            # Create a session
            session = sessionmaker(bind=self.engine)()

            # Return the input object with specific url
            result_input : TENN_Input = session.query(TENN_Input).filter(TENN_Input.input_id == passed_id).first()
            if self.verbose: print("TENN_InputDB - get_input_by_id - Returned: " + str(result_input))

            # Return the input
            return result_input
        except:
            if self.verbose: print("TENN_InputDB - get_input_by_id - Error adding input to the database.")
            return None
        finally:
            session.close()  # Make sure to close the session when done

    #########################################################################################################

    # Function to get the input object for an input aid in the database

    def get_input(self, passed_aid : str = "") -> TENN_Input:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the passed url is None
        if passed_aid is None or passed_aid == "":
            if self.verbose: print("TENN_InputDB - get_input - The passed aid is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Return the input object with specific url
        result_input : TENN_Input = session.query(TENN_Input).filter(TENN_Input.aid == passed_aid).first()
        session.close()
        if self.verbose: print("TENN_InputDB - get_input - Returned: " + str(result_input))

        # Return the input
        return result_input

    #########################################################################################################

    # Function to get the input object for a URL in the database

    def get_input_by_url(self, passed_url : str = "") -> TENN_Input:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the passed url is None
        if passed_url is None or passed_url == "":
            if self.verbose: print("TENN_InputDB - get_input_by_url - The passed url is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Return the input object with specific url
        result_input : TENN_Input = session.query(TENN_Input).filter(TENN_Input.url == passed_url).first()
        session.close()
        if self.verbose: print("TENN_InputDB - get_input_by_url - Returned: " + str(result_input))

        # Return the input
        return result_input

    #########################################################################################################

    # Function to get the input object for a hashcode in the database

    def get_input_by_hashcode(self, passed_hashcode : str = "") -> TENN_Input:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the passed url is None
        if passed_hashcode is None or passed_hashcode == "":
            if self.verbose: print("TENN_InputDB - get_input_by_hashcode - The passed hashcode is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Return the input object with specific url
        result_input : TENN_Input = session.query(TENN_Input).filter(TENN_Input.hashcode == passed_hashcode).first()
        session.close()
        if self.verbose: print("TENN_InputDB - get_input_by_hashcode - Returned: " + str(result_input))

        # Return the input
        return result_input

    #########################################################################################################

    # Function to check if input exists for a URL in the database

    def input_exists_for_url(self, passed_url : str = "") -> bool:

        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the input exists
        if self.verbose: print("TENN_InputDB - input_exists_for_url - Checking if input exists for url: " + passed_url)
        result_input = self.get_input_by_url(passed_url)

        # Return the input
        if result_input is None:
            return False
        else:
            return True

    #########################################################################################################

    # Function to check if input exists for a hashcode in the database

    def input_exists_for_hashcode(self, passed_hashcode : str = "") -> bool:
            
        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the input exists
        if self.verbose: print("TENN_InputDB - input_exists_for_hashcode - Checking if input exists for hashcode: " + passed_hashcode)
        result_input = self.get_input_by_hashcode(passed_hashcode)

        # Return the input
        if result_input is None:
            return False
        else:
            return True


    #########################################################################################################

    # Function to delete input by aid

    def delete_input(self, passed_aid : str = ""):
                
        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the passed aid is None
        if passed_aid is None or passed_aid == "":
            if self.verbose: print("TENN_InputDB - delete_input - The passed aid is None.")
            return None

        if self.verbose: print ("TENN_InputDB - delete_input - Deleting input for aid: " + str(passed_aid))

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the input
        result_input = self.get_input(passed_aid)

        # If the input exists, delete it
        if result_input is not None:
            session.delete(result_input)
            session.commit()
            session.close()

        else:
            if self.verbose: print("TENN_InputDB - delete_input - The input does not exist in the database. Skipping.")

    #########################################################################################################

    # Function to delete input by url

    def delete_input_by_url(self, passed_url : str = ""):
                
        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Check if the passed aid is None
        if passed_url is None or passed_url == "":
            if self.verbose: print("TENN_InputDB - delete_input_by_url - The passed url is None.")
            return None

        if self.verbose: print ("TENN_InputDB - delete_input_by_url - Deleting input for url: " + passed_url)

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the input
        result_input = self.get_input_by_url(passed_url)

        # If the input exists, delete it
        if result_input is not None:
            session.delete(result_input)
            session.commit()
            session.close()

        else:
            if self.verbose: print("TENN_InputDB - delete_input_by_url - The input does not exist in the database. Skipping.")
    
    #########################################################################################################

    # Function to return a list of all input in the database

    def get_all_inputs(self) -> list[TENN_Input]:
               
        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get all the input
        result_input_list = session.query(TENN_Input).all()
        session.close()

        # Return the input
        return result_input_list

    #########################################################################################################

    # Function to return a list of all input in the database based on a list of urls

    def get_all_inputs_for_urls(self, passed_urls : list = None) -> list[TENN_Input]:
               
        # Check if we're connected to the database, if not, connect
        if self.engine is None:
            self.engine = self.connect()
            
        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get all the input
        # TODO Change this to use the passed_urls as a filter / filter(TENN_Input.url in passed_urls).all()
        result_input_list = session.query(TENN_Input).all()
        session.close()

        # Return the input
        return result_input_list
