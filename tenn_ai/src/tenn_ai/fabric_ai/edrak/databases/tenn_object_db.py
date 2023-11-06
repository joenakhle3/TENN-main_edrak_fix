# class that manages the tenn objects in the fabric, based on the TENN_NoSqlDB

import os
import sys
import json
from bson import ObjectId

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.stores.tenn_nosql_db import TENN_NoSqlDB

#########################################################################################################

# This is the structure of the TENN_Object JSON object that will be used to store the data

"""
Example of a TENN_Object JSON object:
{
  "_id": ObjectId,
  "aid": str (uuid4),
  "content_type": str,
  "contents": "Contents of the object, which could be text, image, video, audio, json or binary",
}
"""

#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

# Class that defines the object that is stored in the mongodb database of type TENN_ObjectDB which is based on TENN_NoSqlDB
# This object should have an automatically generated objectID, plus the AID and URL from the TENN_EdrakDB and the full contents of the object whether text, image, video, audio, json or binary

class TENN_Object():
    def __init__(self, passed_data = None, passed_verbose=False):
        # Convert the passed_data to a JSON string
        if passed_data is None:
            passed_data = {}
        elif isinstance(passed_data, str):
            passed_data = json.loads(passed_data)
        elif isinstance(passed_data, dict):
            pass
        
        self.object_data = {
            "aid": "",
            "content_type": "",
            "contents": None
        }
        self.object_data.update(passed_data)
        self.verbose = passed_verbose

    def __repr__(self):
        return self.object_data.__repr__()

    ########################################################################
    # Getter and setter for the object_data property
    @property
    def object_data(self):
        return self._object_data

    @object_data.setter
    def object_data(self, value):
        if value is None:
            value = {}
        elif isinstance(value, str):
            value = json.loads(value)
        elif isinstance(value, dict):
            pass

        self._object_data = value

    # Getter and setter for the verbose property
    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        if not isinstance(value, bool):
            raise TypeError("verbose must be a boolean")
        self._verbose = value

    ########################################################################
    # Getter and setter for the object_id property
    @property
    def object_id(self):
        return self.object_data["_id"]

    @object_id.setter
    def object_id(self, value):
        self.object_data["_id"] = value

    # Getter and setter for the aid property
    @property
    def aid(self):
        return self.object_data["aid"]

    @aid.setter
    def aid(self, value):
        self.object_data["aid"] = value

    # Getter and setter for the content_type property
    @property
    def content_type(self):
        return self.object_data["content_type"]

    @content_type.setter
    def content_type(self, value):
        self.object_data["content_type"] = value

    # Getter and setter for the contents property
    @property
    def contents(self):
        return self.object_data["contents"]

    @contents.setter
    def contents(self, value):
        self.object_data["contents"] = value

    ############################################################################
    # Serialization to JSON
    def to_json(self):
        return json.dumps(self.object_data, indent=4)

    ############################################################################
    # Deserialization from JSON
    @classmethod
    def from_json(cls, json_str):
        object_data = json.loads(json_str)
        return cls(object_data)

    ############################################################################
    # Serialization to dict
    def to_dict(self):
        return self.object_data

#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################    
    
# Class that extends TENN_NoSqlDB to create all the functions of a Object DB

# #########################################################################################################

class TENN_ObjectDB(TENN_NoSqlDB):
        
    # Initiatlize the class with the database type
    def __init__(self, passed_db_hostname="", passed_db_port=0, passed_db_engine="", passed_verbose=False):

        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        # Call the constructor of the parent class (TENN_NoSqlDB)
        super().__init__(passed_db_hostname, passed_db_port, passed_db_engine, passed_verbose)
        self.db_name = self.properties.standard_object_db_name

    
    ############################################################################
    # Override the get_collection method to use the ObjectDB database and collection
    def get_collection(self, passed_collection_name: str):
        return super().get_or_create_collection(passed_collection_name=passed_collection_name, passed_database_name=self.db_name)

    ############################################################################
    # Function to check if an object exists in the database, based on its AID
    def object_exists(self, passed_aid: str, passed_collection_name: str) -> bool:

        if passed_aid is not None and passed_aid != "" and passed_collection_name is not None and passed_collection_name != "":
            # Check if the Object exists in the database
            found_list = super().search_documents(passed_property="aid", passed_value=passed_aid, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
            if found_list is None or found_list.__len__() == 0:
                if self.verbose: print("TENN_ObjectDB - object_exists - Object with AID " + passed_aid + " not found in the database.")
                return False
            else:
                if self.verbose: print("TENN_ObjectDB - object_exists - Object with AID " + passed_aid + " found in the database.")
                return True
        else:
            if self.verbose: print("TENN_ObjectDB - object_exists - Empty arguments passed")
            return False

    ############################################################################
    # Add Object to the database, if it doesn't already exist
    def add_object(self, passed_object : TENN_Object, passed_collection_name: str):

        # If the passed object is None or it doesn't have an AID, then return None
        if passed_object is None or passed_object.aid is None or passed_object.aid == "":
            if self.verbose: print("TENN_ObjectDB - add_object - Object is None or doesn't have an AID. Skipping.")
            return None
        
        # Check if this Object already exists in the database
        if self.object_exists(passed_aid=passed_object.aid, passed_collection_name=passed_collection_name):
            if self.verbose: print("TENN_ObjectDB - add_object - Object with AID " + passed_object.aid + " already exists in the database. Skipping.")
            return None

        if self.verbose: print("TENN_ObjectDB - add_object - Adding Object with AID " + passed_object.aid + " to the database.")
        return super().insert_document(passed_document=passed_object.to_dict(), passed_collection_name=passed_collection_name, passed_database_name=self.db_name)

    ############################################################################
    # Add Object to the database but choose the collection automatically based on the content_type
    def add_object_core(self, passed_object : TENN_Object):

        # If the passed object is None or it doesn't have an AID, then return None
        if passed_object is None or passed_object.aid is None or passed_object.aid == "":
            if self.verbose: print("TENN_ObjectDB - add_object_core - Object is None or doesn't have an AID. Skipping.")
            return None
        
        # If the passed object content_type is none or is not in the keys of properties.content_types_and_core_collection then return None
        if passed_object.content_type is None or passed_object.content_type =="" or passed_object.content_type not in self.properties.content_types_and_core_collection.keys():
            if self.verbose: print("TENN_ObjectDB - add_object_core - Object content_type " + passed_object.content_type + " is invalid or not supported. Skipping.")
            return None
        
        # Add the object to the database, but pick the collection automatically using the properties.content_types_and_core_collection
        collection_name = self.utils.get_core_collection_name_for_content_type(passed_content_type=passed_object.content_type)
        if self.verbose: print("TENN_ObjectDB - add_object_core - Adding Object with AID " + passed_object.aid + " to the database in collection " + collection_name)
        return self.add_object(passed_object=passed_object, passed_collection_name=collection_name)
    
    ############################################################################
    # Delete Object from the database by its aid
    def delete_object(self, passed_aid: str, passed_collection_name: str):

        if passed_aid is not None and passed_aid != "" and passed_collection_name is not None and passed_collection_name != "":

            # Delete the Object data from the database by its ID
            if self.verbose: print("TENN_ObjectDB - delete_object - Deleting Object with AID " + passed_aid + " from the database.")
            return super().delete_documents_by_tuples(passed_dict={"aid": passed_aid}, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return False

    ############################################################################
    # Delete Object from the database by its object_id
    def delete_object_by_id(self, passed_object_id: ObjectId, passed_collection_name: str):

        if passed_object_id is not None and passed_collection_name is not None and passed_collection_name != "":

            # Delete the Object data from the database by its ID
            if self.verbose: print("TENN_ObjectDB - delete_object_by_id - Deleting Object with ID " + str(passed_object_id) + " from the database.")
            return super().delete_document(passed_document_id=passed_object_id, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return False

    ############################################################################
    # Modify Object data in the database
    def modify_object(self, passed_aid: str, passed_new_object : TENN_Object, passed_collection_name: str):

        if passed_aid is not None and passed_aid != "" and passed_collection_name is not None and passed_collection_name != "":

            # Update the Object data in the database
            if self.verbose: print("TENN_ObjectDB - modify_object - Modifying Object with AID " + passed_aid + " in the database.")
            return super().update_documents_by_tuples(passed_dict={"aid": passed_aid}, passed_new_document=passed_new_object.to_dict(), passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return False
    
    ############################################################################
    # Modify Object data in the database
    def modify_object_by_id(self, passed_object_id: ObjectId, passed_new_object : TENN_Object, passed_collection_name: str):

        if passed_object_id is not None and passed_collection_name is not None and passed_collection_name != "":

            # Update the Object data in the database
            if self.verbose: print("TENN_ObjectDB - modify_object_by_id - Modifying Object with ID " + str(passed_object_id) + " in the database.")
            return super().update_document(passed_document_id=passed_object_id, passed_new_document=passed_new_object.to_dict(), passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return False

    ############################################################################
    # Get Object data from the database by its unique identifier
    def get_object(self, passed_aid: str, passed_collection_name: str) -> TENN_Object:

        if passed_aid is not None and passed_aid != "" and passed_collection_name is not None and passed_collection_name != "":

            # Get the Object data from the database by its ID
            if self.verbose: print("TENN_ObjectDB - get_object - Getting Object with AID " + passed_aid + " from the database.")
            document : dict = super().get_document_by_property(passed_property="aid", passed_value=passed_aid, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)

            # check if the document is not None
            if document is None:
                if self.verbose: print("TENN_ObjectDB - get_object - Object with AID " + passed_aid + " not found in the database.")
                return None
            else:
                return TENN_Object(passed_data=document, passed_verbose=self.verbose)
        else:
            return None
                
    ############################################################################
    # Get Object data from the database by its unique identifier
    def get_object_by_id(self, passed_object_id: ObjectId, passed_collection_name: str) -> TENN_Object:

        if passed_object_id is not None and passed_collection_name is not None and passed_collection_name != "":

            # Get the Object data from the database by its ID
            document : dict = super().get_document(passed_document_id=passed_object_id, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)

            # check if the document is not None
            if document is None:
                return None
            else:
                return TENN_Object(passed_data=document, passed_verbose=self.verbose)
        else:
            return None
    
    ############################################################################
    # Search for Objects based on its content
    def search(self, passed_search_query: dict, passed_collection_name: str) -> list:
        if passed_search_query is not None and passed_collection_name is not None and passed_collection_name != "":

            # Construct a search_dict based on the search_query
            search_dict = {}  # Initialize an empty dictionary
            for key, value in passed_search_query.items():
                search_dict[key] = value

            # Call the search_documents_by_tuples function with the constructed search_dict
            return super().search_documents_by_tuples(passed_dict=search_dict, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return None

    ############################################################################ 
    # Count the number of Objects in the database
    def count_objects(self, passed_dict: dict, passed_collection_name: str) -> int:
        if passed_dict is not None and passed_collection_name is not None and passed_collection_name != "":

            # Call the count_documents_by_tuples function with the constructed search_dict
            return super().count_documents_by_tuples(passed_dict=passed_dict, passed_collection_name=passed_collection_name, passed_database_name=self.db_name)
        else:
            return None