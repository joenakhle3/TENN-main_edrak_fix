

import os
import sys
import json
import datetime
import time
import uuid

# Import TENN classes
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties 
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils 
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB

# Import SQLalchemy
from sqlalchemy import Engine, Table, Column
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Initialize the declarative base for sqlalchemy
Base = declarative_base()

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

# The Awareness class is the master record for any awareness that is create from any input
class TENN_Tag(Base):

    # Define the table name in the database
    __tablename__ = 'tags'

    # Define the table columns
    tag_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tag_name = Column(String(50), nullable=False, unique=True)
    tag_description = Column(String(255), nullable=True)
    tag_parent_tag_id = Column(Integer, ForeignKey("tags.tag_id"), nullable=False, default=0)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)

    # Define the one-to-many relationship
    awareness_tags = relationship("TENN_AwarenessTag", back_populates="tag")

    #########################################################################################################

    # Define the constructor
    def __init__(self, passed_tag_name: str = "", passed_tag_description: str = "", passed_tag_parent_id: int = 0):
        self.tag_name = passed_tag_name
        self.tag_description = passed_tag_description
        self.tag_parent_tag_id = passed_tag_parent_id
        self.active = True 

    #########################################################################################################

    # Define the string representation of the object
    def __repr__(self):
        return "<TENN_Tag(tag_name='%s', tag_description='%s', tag_parent_tag_id='%s')>" % (
         self.tag_name, self.tag_description, self.tag_parent_tag_id)
    
    def create_tag(self, session):
        try:
            # Create a new instance of TENN_Tag
            new_tag = TENN_Tag(self.tag_name, self.tag_description, self.tag_parent_tag_id)

            # Add the new tag to the session and commit the transaction
            session.add(new_tag)
            session.commit()

            return new_tag
        except Exception as e:
            session.rollback()
            raise e
        
    #########################################################################################################

class TENN_AwarenessTag(Base):
    __tablename__ = 'awareness_tags'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    awareness_id = Column(String(36), ForeignKey('awareness.aid'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), nullable=False)

    awareness = relationship("TENN_Awareness", back_populates="awareness_tags")
    tag = relationship("TENN_Tag", back_populates="awareness_tags")
    
#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################

# Class that extends TENN_SqlDB to create all needed functions of the Organize DB

# #########################################################################################################

class TENN_OrganizeDB(TENN_SqlDB):
    def __init__(self, database_path: str,passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):
        super().__init__(passed_db_path, passed_db_engine, passed_verbose)
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.database_path = database_path

    #########################################################################################################

    def connect(self) -> Engine:
        self.engine = super().connect()
        Base.metadata.create_all(self.engine)    

        return self.engine

    #########################################################################################################

    # Add a new tag to the database
    # Returns the tag_id
    #  
    def add_or_update_tag(self, passed_tag: TENN_Tag = None) -> int:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_OrganizeDB - add_or_update_tag - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed awareness is None
        if passed_tag is None:
            if self.verbose: print("TENN_OrganizeDB - add_or_update_tag - The passed tag is None.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        try:
            with session:
                # Add the awareness to the database
                session.add(passed_tag)

            # Return the aid
            return passed_tag.tag_id
        
        except:
            if self.verbose: print("TENN_OrganizeDB - add_or_update_tag - Error adding tag to the database.")
            return None
        
        finally:
            session.commit()
            session.close()

