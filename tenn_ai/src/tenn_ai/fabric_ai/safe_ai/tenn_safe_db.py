import os
import sys
import json
import datetime
import time
import uuid
from typing import AsyncGenerator, Optional, List, Dict

# Import TENN classes
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB

# Import SQLalchemy
from sqlalchemy import Engine, Table, Column, func
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Import fastapi classes
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users import schemas
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

class UserRead(schemas.BaseUser[uuid.UUID]):
    # Define the table columns

    # id UUID is already in the base class
    # email str already in the base class
    # password already in the base class
    # is_active bool already in the base class, defaults to True
    # is_verified bool already in the base class, defaults to False
    # is_superuser bool already in the base class, defaults to False
    first_name = str
    last_name = str
    mobile = str
    city = Optional[str]
    country = Optional[str]
    birthdate = Optional[datetime.date]
    org_id = int
    created = datetime.datetime
    updated = datetime.datetime

class UserCreate(schemas.BaseUserCreate):
    first_name = str
    last_name = str
    mobile = Optional[str]
    city = Optional[str]
    country = Optional[str]
    birthdate = Optional[datetime.date]
    org_id = int

class UserUpdate(schemas.BaseUserUpdate):
    first_name = Optional[str]
    last_name = Optional[str]
    mobile = Optional[str]
    city = Optional[str]
    country = Optional[str]
    birthdate = Optional[datetime.date]
    org_id = Optional[int]

# Initialize the declarative base for sqlalchemy
class Base(DeclarativeBase):
    pass

class TENN_User(SQLAlchemyBaseUserTableUUID, Base):
    pass

async def get_safe_db_url() -> str:
    properties = TENN_Properties()
    return properties.standard_edrak_db_path + ":///" + properties.standard_edrak_db_engine

safeDB_engine = create_async_engine(get_safe_db_url())
async_session_maker = async_sessionmaker(safeDB_engine, expire_on_commit=False)

async def create_db_and_tables():
    async with safeDB_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, TENN_User)

#########################################################################################################

# The User class is the master record for any user that is created 
class TENN_User_Original(Base):

    # Define the table name in the database
    __tablename__ = 'users'

    # Define the table columns
    email = Column(String(255), primary_key=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    org_id = Column(Integer, ForeignKey("orgs.org_id"), nullable=False, default=1) # 1 is the root parent
    enabled = Column(Boolean, nullable=False, default=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################
    # Define the constructor

    def __init__(self, passed_email: str = "", passed_password: str = "", passed_username: str = "", passed_first_name: str = "", passed_last_name: str = "", passed_mobile: str = "", passed_city: str = "", passed_country: str = "", passed_org_id: int = 0):
        self.email = passed_email
        self.password = passed_password
        self.username = passed_username
        self.first_name = passed_first_name
        self.last_name = passed_last_name
        self.mobile = passed_mobile
        self.city = passed_city
        self.country = passed_country
        self.org_id = passed_org_id

    #########################################################################################################
    # Define the string representation of the object

    def __repr__(self):
        return "<TENN_User(email='%s', password='%s', username='%s', first_name='%s', last_name='%s', mobile='%s', city='%s', country='%s', org_id='%s', created='%s', updated='%s')>" % (self.email, self.password, self.username, self.first_name, self.last_name, self.mobile, self.city, self.country, self.org_id, self.created, self.updated)

    #########################################################################################################
    # Define the dict representation of the object

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mobile": self.mobile,
            "city": self.city,
            "country": self.country,
            "org_id": self.org_id,
            "created": self.created,
            "updated": self.updated
        }
    
    #########################################################################################################
    # Define the from_dict loading of the object

    def from_dict(self, passed_dict: dict):
        self.email = passed_dict["email"]
        self.password = passed_dict["password"]
        self.username = passed_dict["username"]
        self.first_name = passed_dict["first_name"]
        self.last_name = passed_dict["last_name"]
        self.mobile = passed_dict["mobile"]
        self.city = passed_dict["city"]
        self.country = passed_dict["country"]
        self.org_id = passed_dict["org_id"]

#########################################################################################################
# The Org class is the master record for any organization that is created

class TENN_Org(Base): 

    # Define the table name in the database
    __tablename__ = 'orgs'

    # Define the table columns
    org_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    main_phone = Column(String(50), nullable=False)
    main_email = Column(String(255), nullable=False)
    support_phone = Column(String(50), nullable=False)
    support_email = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    pobox = Column(String(20), nullable=False)
    website = Column(String(255), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################
    # Contructor

    def __init__(self, passed_name: str = "", passed_description: str = "", passed_main_phone: str = "", passed_main_email: str = "", passed_support_phone: str = "", passed_support_email: str = "", passed_address: str = "", passed_city: str = "", passed_country: str = "", passed_website: str = ""):
        self.name = passed_name
        self.description = passed_description
        self.main_phone = passed_main_phone
        self.main_email = passed_main_email
        self.support_phone = passed_support_phone
        self.support_email = passed_support_email
        self.address = passed_address
        self.city = passed_city
        self.country = passed_country
        self.website = passed_website

    #########################################################################################################
    # Representation

    def __repr__(self):
        return "<TENN_Org(org_id='%s', name='%s', description='%s', main_phone='%s', main_email='%s', support_phone='%s', support_email='%s', address='%s', city='%s', country='%s', website='%s')>" % (self.org_id, self.name, self.description, self.main_phone, self.main_email, self.support_phone, self.support_email, self.address, self.city, self.country, self.website)

    #########################################################################################################
    # Define the dict representation of the object

    def to_dict(self):
        return {
            "org_id": self.org_id,
            "name": self.name,
            "description": self.description,
            "main_phone": self.main_phone,
            "main_email": self.main_email,
            "support_phone": self.support_phone,
            "support_email": self.support_email,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "website": self.website,
            "created": self.created,
            "updated": self.updated
        }

#########################################################################################################

class TENN_User_Org_Relationship(Base):

    # Define the table name in the database
    __tablename__ = 'user_org_relationship'

    # Define the table columns
    user_org_relationship_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    org_id = Column(Integer, ForeignKey("orgs.org_id"), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = Column(DateTime, nullable=False, default=datetime.datetime.utcnow) # TODO make this a trigger

    #########################################################################################################

    # Define the constructor
    def __init__(self, passed_tag_id: int = 0, passed_user_id: int = 0):
        self.tag_id = passed_tag_id
        self.user_id = passed_user_id

    #########################################################################################################

    # Define the string representation of the object
    def __repr__(self):
        return "<TENN_Tag_AID_Relationship(tag_user_id_relationship_id='%s', tag_id='%s', user_id='%s', created='%s', updated='%s')>" % (
            self.tag_user_id_relationship_id, self.tag_id, self.user_id, self.created, self.updated)

#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################

# Class that extends TENN_SqlDB to create all needed functions of the Organize DB

# #########################################################################################################

class TENN_SafeDB(TENN_SqlDB):
    
    #########################################################################################################

    # Initiatlize the class with the database type
    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):

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

    # Add a new user to the database
    # Returns the user id 
    def add_or_update_user(self, passed_user: TENN_User = None) -> TENN_User:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - add_or_update_user - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed user is None
        if passed_user is None:
            if self.verbose: print("TENN_SafeDB - add_or_update_user - The passed user is None.")
            return None

        try:
            # Convert the email to lowercase
            passed_user.email = passed_user.email.strip().lower()

            # Create a session
            session = sessionmaker(bind=self.engine)()

            # Add the user to the database
            session.add(passed_user)
            session.commit()

            # Return the user_id
            return passed_user
        
        except:
            if self.verbose: print("TENN_SafeDB - add_or_update_user - Error adding user to the database.")
            return None

    #########################################################################################################

    # Function to get the user for an email in the database

    def get_user(self, passed_email : str = "") -> TENN_User:

        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - get_user - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed email is None
        if passed_email is None or passed_email == "":
            if self.verbose: print("TENN_SafeDB - get_user - The passed email is empty.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Check if the user exists
        result_user = session.query(TENN_User).filter(TENN_User.email == passed_email.strip().lower()).first()
        if self.verbose: print("TENN_SafeDB - get_user - Returned user with email: " + str(result_user.email))

        # Return the user
        return result_user

    #########################################################################################################

    # Function to get the user for a username in the database

    def get_user_by_username(self, passed_username : str = "") -> TENN_User:

        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - get_user_by_username - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed username is None
        if passed_username is None or passed_username == "":
            if self.verbose: print("TENN_SafeDB - get_user_by_username - The passed username is empty.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Check if the user exists
        result_user = session.query(TENN_User).filter(TENN_User.username == passed_username.strip()).first()
        if self.verbose: print("TENN_SafeDB - get_user_by_username - Returned user with email: " + str(result_user.email))

        # Return the user
        return result_user


    #########################################################################################################

    # Function to check if user exists for a email in the database

    def user_exists(self, passed_email : str = "") -> bool:
            
        # Check if the user exists
        if self.verbose: print("TENN_SafeDB - user_exists - Checking if user exists for email: " + passed_email)
        return (self.get_user(passed_email) is not None)

    #########################################################################################################

    # Function to check if user exists for a username in the database

    def username_exists(self, passed_username : str = "") -> bool:
            
        # Check if the user exists
        if self.verbose: print("TENN_SafeDB - username_exists - Checking if user exists for email: " + passed_username)
        return (self.get_user_by_username(passed_username) is not None)

    #########################################################################################################

    # Function to delete all user for a email from the database

    def delete_user(self, passed_email : str = None) -> bool:
            
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - delete_user - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed email is None
        if passed_email is None or passed_email == "":
            print("TENN_SafeDB - delete_user - The passed email is empty.")
            return False

        if self.verbose: print ("TENN_SafeDB - delete_user - Deleting user for email: " + passed_email)

        # Get the user
        result_user = self.get_user(passed_email=passed_email)

        # If the user exists, delete it
        if result_user is not None:
            # Create a session
            session = sessionmaker(bind=self.engine)()
            session.delete(result_user)
            session.commit()
            return True
        else:
            if self.verbose: print("TENN_SafeDB - delete_user - The user does not exist in the database. Skipping.")
            return False
    
    #########################################################################################################

    # Function to return a list of all user in the database

    def get_all_users(self) -> list[TENN_User]:
               
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - get_all_users - Not connected to the database. Connecting.")
            self.connect()

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get all the user
        result_user_list = session.query(TENN_User).all()

        # Return the user
        return result_user_list
    

    #########################################################################################################
    #########################################################################################################
    #########################################################################################################

    # Add a new org to the database
    # Returns the org id 
    def add_or_update_org(self, passed_org: TENN_Org = None) -> int:
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - add_or_update_org - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed org is None
        if passed_org is None:
            if self.verbose: print("TENN_SafeDB - add_or_update_org - The passed org is None.")
            return None

        try:
            # Create a session
            session = sessionmaker(bind=self.engine)()

            # Add the org to the database
            session.add(passed_org)
            session.commit()

            # Return the org_id
            return passed_org.org_id
        
        except:
            if self.verbose: print("TENN_SafeDB - add_or_update_org - Error adding org to the database.")
            return 0

    #########################################################################################################

    # Function to get the org object by its org_id

    def get_org(self, passed_org_id : int = 0) -> TENN_Org:
                
            # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - get_org - Not connected to the database. Connecting.")
            self.connect()
    
        # Check if the passed org_id is None
        if passed_org_id is None or passed_org_id == 0:
            if self.verbose: print("TENN_SafeDB - get_org - The passed org_id is empty.")
            return None

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get the org
        result_org = session.query(TENN_Org).filter(TENN_Org.org_id == passed_org_id).first()
        if self.verbose: print("TENN_SafeDB - get_org - Returned org_id: " + str(result_org.org_id))

        # Return the org
        return result_org

    #########################################################################################################

    # Function to check if org exists for a email in the database

    def org_exists(self, passed_org_id : int = 0) -> bool:
            
        # Check if the org exists
        if self.verbose: print("TENN_SafeDB - org_exists - Checking if org exists for id: " + passed_org_id)
        result_org = self.get_org(passed_org_id)

        # Return the org
        if result_org is None:
            return False
        else:
            return True

    #########################################################################################################

    # Function to delete org by org_id

    def delete_org(self, passed_org_id : int = 0) -> bool:
                
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - delete_org - Not connected to the database. Connecting.")
            self.connect()

        # Check if the passed org_id is None
        if passed_org_id is None or passed_org_id == 0:
            if self.verbose: print("TENN_SafeDB - delete_org - The passed org_id is empty.")
            return False

        print ("TENN_SafeDB - delete_org - Deleting org for org_id: " + str(passed_org_id))

        # Get the org
        result_org = self.get_org(passed_org_id=passed_org_id)

        # If the org exists, delete it
        if result_org is not None:
            # Create a session
            session = sessionmaker(bind=self.engine)()
            session.delete(result_org)
            session.commit()
            return True
        else:
            if self.verbose: print("TENN_SafeDB - delete_org - The org does not exist in the database. Skipping.")
            return False
    
    #########################################################################################################

    # Function to return a list of all org in the database

    def get_all_orgs(self) -> list[TENN_Org]:
               
        # Check if we're connected to the database
        if self.engine is None:
            if self.verbose: print("TENN_SafeDB - get_all_orgs - Not connected to the database. Connecting.")
            self.connect()

        # Create a session
        session = sessionmaker(bind=self.engine)()

        # Get all the org
        result_org_list = session.query(TENN_Org).all()

        # Return the org
        return result_org_list
    

