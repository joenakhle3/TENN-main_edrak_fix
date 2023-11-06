import os
import sys
import json
import datetime
import time
import uuid

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties as properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils as utils
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB

from sqlalchemy import Engine, Table, Column
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Initialize the declarative base for sqlalchemy
Base = declarative_base()

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

# The Awareness class is the master record for any awareness that is create from any input
class TENN_Prompt(Base):

    # Define the table name in the database
    __tablename__ = 'prompts'

    # Define the table columns
    prompt_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    prompt_name = Column(String(50), nullable=True, unique=True)
    prompt_description = Column(String(255), nullable=True)
    prompt_type = Column(CHAR, nullable=True) # I or O for input or output
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################

    # Define the constructor
    def __init__(self, passed_prompt_url: str = "", passed_prompt_aid: UUID = None, passed_prompt_name: str = "", passed_prompt_description: str = "", passed_prompt_type: CHAR = "O"):
        self.prompt_url = passed_prompt_url
        self.prompt_aid = passed_prompt_aid
        self.prompt_name = passed_prompt_name
        self.prompt_description = passed_prompt_description
        self.prompt_type = passed_prompt_type

    #########################################################################################################

    # Define the string representation of the object
    def __repr__(self):
        return "<TENN_Prompt(prompt_id='%s', prompt_url='%s', prompt_aid='%s', prompt_name='%s', prompt_description='%s', prompt_type='%s', created='%s', updated='%s')>" % (
            self.prompt_id, self.prompt_url, self.prompt_aid, self.prompt_name, self.prompt_description, self.prompt_type, self.created, self.updated)

#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################

# Class that extends TENN_SqlDB to create all the functions of a Prompt DB

# #########################################################################################################

class TENN_PromptDB(TENN_SqlDB):
    
    # Initiatlize the class with the database type
    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):

        super().__init__(passed_db_path, passed_db_engine, passed_verbose)

    ##############################################################################################################################

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

    # Add a new prompt to the database
    def add_or_update_prompt(self, passed_prompt: TENN_Prompt = None) -> int:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_PromptDB - add_or_update_prompt - Not connected to the database. Please connect() first.")
            return None

        # Check if the passed awareness is None
        if passed_prompt is None:
            if self.verbose: print("TENN_PromptDB - add_or_update_prompt - The passed awareness is None.")
            return None

        try:
            # Create a session
            session = sessionmaker(bind=self.engine)()

            # Add the awareness to the database
            session.add(passed_prompt)
            session.commit()

            # Return the aid
            return passed_prompt.prompt_id
        
        except:
            if self.verbose: print("TENN_PromptDB - add_or_update_prompt - Error adding awareness to the database.")
            return None

    #########################################################################################################

