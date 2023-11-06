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
class TENN_Template(Base):

    # Define the table name in the database
    __tablename__ = 'templates'

    # Define the table columns
    template_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    template_url = Column(String(512), nullable=False, unique=True) # TODO change this later into a relationship with an Input object
    template_aid = Column(UUID(as_uuid=True), nullable=True, unique=True)
    template_name = Column(String(50), nullable=True, unique=True)
    template_description = Column(String(255), nullable=True)
    template_type = Column(CHAR, nullable=True) # I or O for input or output
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################

    # Define the constructor
    def __init__(self, passed_template_url: str = "", passed_template_aid: UUID = None, passed_template_name: str = "", passed_template_description: str = "", passed_template_type: CHAR = "O"):
        self.template_url = passed_template_url
        self.template_aid = passed_template_aid
        self.template_name = passed_template_name
        self.template_description = passed_template_description
        self.template_type = passed_template_type

    #########################################################################################################

    # Define the string representation of the object
    def __repr__(self):
        return "<TENN_Template(template_id='%s', template_url='%s', template_aid='%s', template_name='%s', template_description='%s', template_type='%s', created='%s', updated='%s')>" % (
            self.template_id, self.template_url, self.template_aid, self.template_name, self.template_description, self.template_type, self.created, self.updated)

#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################


# Class that extends TENN_SqlDB to create all the functions of a Template DB

# #########################################################################################################

class TENN_TemplateDB(TENN_SqlDB):
    
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

    # Add a new template to the database
    def add_or_update_template(self, passed_template: TENN_Template = None) -> int:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_TemplateDB - add_or_update_template - Not connected to the database. Please connect() first.")
            return None

        # Check if the passed awareness is None
        if passed_template is None:
            if self.verbose: print("TENN_TemplateDB - add_or_update_template - The passed awareness is None.")
            return None

        try:
            # Create a session
            session = sessionmaker(bind=self.engine)()

            # Add the awareness to the database
            session.add(passed_template)
            session.commit()

            # Return the aid
            return passed_template.template_id
        
        except:
            if self.verbose: print("TENN_TemplateDB - add_or_update_template - Error adding awareness to the database.")
            return None

    #########################################################################################################

