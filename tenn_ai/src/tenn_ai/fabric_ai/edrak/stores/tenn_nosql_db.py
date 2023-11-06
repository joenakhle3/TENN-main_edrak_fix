import os
import sys
import json
import uuid

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties

from pymongo import MongoClient
from bson import ObjectId

class TENN_NoSqlDB:

    # #########################################################################################################

    # Initiatlize the class with the database type
    def __init__(self, passed_db_hostname: str = "", passed_db_port: int = 0, passed_db_engine: str = "", passed_verbose: bool = False):
        self.properties = TENN_Properties()

        self.db_engine_type = None
        self.db_hostname = ""
        self.db_port = 0
        self.engine = None # Will be set in the connect() function
        self.verbose = passed_verbose

        # If the passed db engine is none or empty, use the standard object db engine from the properties
        if passed_db_engine is None or passed_db_engine == "":
            self.db_engine_type = self.properties.standard_object_db_engine
        elif passed_db_engine not in self.properties.allowed_engines:
            print("TENN_NoSqlDB - Unsupported database engine type (" + passed_db_engine + "). Switching to standard Object database.")
            self.db_engine_type = self.properties.standard_object_db_engine
        else:
            self.db_engine_type = passed_db_engine
        if self.verbose: print("TENN_NoSqlDB - Using database engine " + self.db_engine_type)

        # If the passed db url is none or empty, use the standard object db path from the properties
        if passed_db_hostname is None or passed_db_hostname == "":
            self.db_hostname = self.properties.standard_object_db_hostname
        else:
            self.db_hostname = passed_db_hostname
        if self.verbose: print("TENN_NoSqlDB - Using database hostname " + self.db_hostname)

        # If the passed db port is 0 or none, use the standard object db port from the properties
        if passed_db_port is None or passed_db_port == 0:
            self.db_port = self.properties.standard_object_db_port
        else:
            self.db_port = passed_db_port
        if self.verbose: print("TENN_NoSqlDB - Using database port " + str(self.db_port))

        # Create the connection string
        self.connection_string = self.db_engine_type + "://" + self.db_hostname + ":" + str(self.db_port) + "/"
        if self.verbose: print("TENN_NoSqlDB - Using connection string " + self.connection_string)

    # #########################################################################################################

    # Set the database engine
    def connect(self):
        # Create the engine based on db_type.
        try:
            self.engine = MongoClient(self.connection_string)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Connect error: " + str(e))
            return None
        
        if self.verbose: print("TENN_NoSqlDB - Connected to the database.")
        return self.engine
                               
        # TODO - Add support for other database types based on the engine type

    # #########################################################################################################

    # Get the passed database from the engine

    def get_or_create_database(self, passed_database_name: str):
        
        # Check if we're connected, if not, connect
        if self.engine is None:
            self.connect()
            
        # If passed_database_name is none or empty, use the standard nosql db name from the properties
        if passed_database_name is None or passed_database_name == "":
            passed_database_name = self.properties.standard_no_sql_db_name
        
        # Get the database from the engine
        try:
            database = self.engine[passed_database_name]
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get database error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Got database " + passed_database_name)
        return database
    
    # #########################################################################################################

    # Get a list of all databases from the engine

    def get_database_list(self):
        # Get the database from the engine
        try:
            database_list = self.engine.list_database_names()
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get database list error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Got database list")
        return database_list

    # #########################################################################################################

    # Check if database exists in the object DB

    def database_exists(self, passed_database_name: str):
        # Get the database from the engine
        database_list = self.get_database_list()

        if passed_database_name in database_list:
            return True
        else:
            return False

    # #########################################################################################################

    # Delete a database

    def delete_database(self, passed_database_name: str):
            
            if self.database_exists(passed_database_name = passed_database_name):
                if self.verbose: print("TENN_NoSqlDB - Database " + passed_database_name + " does not exist")
                return False
            
            # Get the database from the engine
            database = self.get_or_create_database(passed_database_name = passed_database_name)
    
            # Delete the database
            try:
                database.drop_database(passed_database_name)
            except Exception as e:
                if self.verbose: print("TENN_NoSqlDB - Delete database error: " + str(e))
                return False
    
            if self.verbose: print("TENN_NoSqlDB - Deleted database " + passed_database_name)
            return True

    # #########################################################################################################

    # Get or create the passed collection from the database

    def get_or_create_collection(self, passed_collection_name: str, passed_database_name: str = ""):

        # If the collection name is none or empty, return none
        if passed_collection_name is None or passed_collection_name == "":
            if self.verbose: print("TENN_NoSqlDB - Collection name is none or empty")
            return None

        # If the database name is empty, set the standard database name
        db_name = ""
        if passed_database_name == "" or passed_database_name is None:
            db_name = self.properties.standard_no_sql_db_name
        else:
            db_name = passed_database_name.lower()

        database = self.get_or_create_database(passed_database_name = db_name)

        # Get the collection from the database
        try:
            collection = database[passed_collection_name]
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get collection error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Got collection " + passed_collection_name)
        return collection

    # #########################################################################################################

    # Get a list of all collections from the database

    def get_collection_list(self, passed_database_name: str):

        # If the database name is empty, set the standard database name
        db_name = ""
        if passed_database_name == "" or passed_database_name is None:
            db_name = self.properties.standard_no_sql_db_name
        else:
            db_name = passed_database_name.lower()

        # Get the database from the engine
        database = self.get_or_create_database(passed_database_name = db_name)

        # Get the collection from the database
        try:
            collection_list = database.list_collection_names()
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get collection list error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Got collection list")
        return collection_list
    
    # #########################################################################################################

    # Check if collection exists in the object DB in a certain database

    def collection_exists(self, passed_collection_name: str, passed_database_name: str = ""):
        # Get the database from the engine
        collection_list = self.get_collection_list(passed_database_name = passed_database_name)

        if passed_collection_name in collection_list:
            return True
        else:
            return False
        
    # #########################################################################################################

    # Delete a collection

    def delete_collection(self, passed_collection_name: str, passed_database_name: str = ""):

        if not self.collection_exists(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name):
            print("TENN_NoSqlDB - Collection " + passed_collection_name + " does not exist in database " + passed_database_name)
            return False
        
        # Get the database from the engine
        database = self.get_or_create_database(passed_database_name = passed_database_name)

        # Delete the collection
        try:
            database.drop_collection(passed_collection_name)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Delete collection error: " + str(e))
            return False

        if self.verbose: print("TENN_NoSqlDB - Deleted collection " + passed_collection_name + " from database " + passed_database_name)
        return True

    # #########################################################################################################

    # Insert a document into the collection and return its id
    # The id is always automatically created for a document, and it has the format _id 

    def insert_document(self, passed_document: dict, passed_collection_name: str, passed_database_name: str) -> ObjectId:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Insert the document (if it has no _id variable, this will be added automatically)
        try:
            result = collection.insert_one(passed_document)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Insert document error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Inserted document " + str(result.inserted_id))
        return result.inserted_id
    
    # #########################################################################################################

    # Insert a list of documents into the collection and return their ids

    def insert_documents(self, passed_documents: list, passed_collection_name: str, passed_database_name: str) -> list:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Insert the documents
        try:
            result = collection.insert_many(passed_documents)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Insert documents error: " + str(e))
            return None

        if self.verbose: print("TENN_NoSqlDB - Inserted documents " + str(result.inserted_ids))
        return result.inserted_ids
    
    # #########################################################################################################

    # Get a document from the collection based on its id

    def get_document(self, passed_document_id: ObjectId, passed_collection_name: str, passed_database_name: str) -> dict:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Get the document
        try:
            document = collection.find_one({"_id": passed_document_id})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get document error: " + str(e))
            return None
        
        if self.verbose: print("TENN_NoSqlDB - Got document " + str(document))
        return document

    # #########################################################################################################

    # Get a document ID from the collection based on a property and value

    def get_document_id_by_property(self, passed_property: str, passed_value: str, passed_collection_name: str, passed_database_name: str) -> ObjectId:
        # Get the document
        document = self.get_document_by_property(passed_collection_name = passed_collection_name, passed_property = passed_property, passed_value = passed_value, passed_database_name = passed_database_name)

        # Return the document id
        return document["_id"]

    # #########################################################################################################

    # Get a document from the collection based on a property and value

    def get_document_by_property(self, passed_property: str, passed_value: str, passed_collection_name: str, passed_database_name: str) -> dict:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Get the document
        try:
            document = collection.find_one({passed_property: passed_value})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Get document error: " + str(e))
            return None
        
        if self.verbose: print("TENN_NoSqlDB - Got document " + str(document))
        return document

    # #########################################################################################################

    # Count the number of documents in a collection

    def count_documents_by_tuples(self, passed_dict: dict, passed_collection_name: str = "", passed_database_name: str = ""):
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Count the number of documents in the specified collection that have the given key/value pair
        try:
            count = collection.count_documents(passed_dict)
            if self.verbose: print("TENN_NoSqlDB - Counted documents " + str(count))
            return count
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Count documents error: " + str(e))
            return 0

    # #########################################################################################################

    # Search a collection for a list of documents based on a passed property and value

    def search_documents(self, passed_property: str, passed_value: str, passed_sort_by = "_id", passed_descending = False, passed_collection_name: str = "", passed_database_name: str = "") -> list:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Get the documents
        try:
            documents = collection.find({passed_property: passed_value})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Search documents error: " + str(e))
            return None
        
        if self.verbose: print("TENN_NoSqlDB - Got documents " + str(documents))

        if (documents is not None):
            documents = list(documents)
            # TODO documents.sort(key=passed_sort_by, reverse=passed_descending)
            return documents
        else:
            return None

    # #########################################################################################################

    # Search a collection for a list of documents based on a passed dict of properties and values
    # passed_dict should be in the format {"property1": "value1", "property2": "value2"}

    def search_documents_by_tuples(self, passed_dict: dict, passed_sort_by = "_id", passed_descending = False, passed_collection_name: str = "", passed_database_name: str = "") -> list:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Get the documents
        try:
            documents = collection.find(passed_dict)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Search documents error: " + str(e))
            return None
        
        if self.verbose: print("TENN_NoSqlDB - Got documents " + str(documents))

        if documents is not None:
            documents = list(documents)
            # sort the documents by the passed sort_by property
            # TODO documents.sort(key=passed_sort_by, reverse=passed_descending)
            return documents
        else:
            return None

    # #########################################################################################################

    # Delete a document

    def delete_document(self, passed_document_id: ObjectId, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Delete the document
        try:
            result = collection.delete_many({"_id": passed_document_id})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Delete document error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Deleted document " + str(result.deleted_count))
        return True

    # #########################################################################################################

    # Delete a list of documents

    def delete_documents(self, passed_document_ids: list, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Delete the documents
        try:
            result = collection.delete_many({"_id": {"$in": passed_document_ids}})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Delete documents error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Deleted documents " + str(result.deleted_count))
        return True
    
    # #########################################################################################################

    # Delete documents based on a passed dict of properties and values

    def delete_documents_by_tuples(self, passed_dict: dict, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Delete the documents
        try:
            result = collection.delete_many(passed_dict)
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Delete documents error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Deleted documents " + str(result.deleted_count))
        return True

    # #########################################################################################################

    # Delete all documents in a collection

    def delete_all_documents(self, passed_collection_name: str, passed_database_name: str = "") -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Delete the documents
        try:
            result = collection.delete_many({})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Delete documents error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Deleted documents " + str(result.deleted_count))
        return True
    
    # #########################################################################################################

    # Update a document

    def update_document(self, passed_document_id: ObjectId, passed_new_document: dict, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Update the document
        try:
            result = collection.update_one({"_id": passed_document_id}, {"$set": passed_new_document})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Update document error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Updated document " + str(result.modified_count))
        return True
    
    # #########################################################################################################

    # Update a list of documents

    def update_documents(self, passed_document_ids: list, passed_new_document: dict, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Update the documents
        try:
            result = collection.update_many({"_id": {"$in": passed_document_ids}}, {"$set": passed_new_document})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Update documents error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Updated documents " + str(result.modified_count))
        return True
    
    # #########################################################################################################

    # Update documents based on a passed dict of properties and values

    def update_documents_by_tuples(self, passed_dict: dict, passed_new_document: dict, passed_collection_name: str, passed_database_name: str) -> bool:
        # Get the collection
        collection = self.get_or_create_collection(passed_collection_name = passed_collection_name, passed_database_name = passed_database_name)

        # Update the documents
        try:
            result = collection.update_many(passed_dict, {"$set": passed_new_document})
        except Exception as e:
            if self.verbose: print("TENN_NoSqlDB - Update documents error: " + str(e))
            return False
        
        if self.verbose: print("TENN_NoSqlDB - Updated documents " + str(result.modified_count))
        return True
    