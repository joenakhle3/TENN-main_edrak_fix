import os
import sys

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils

import chromadb
from chromadb import Client
from chromadb.utils import embedding_functions
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

#########################################################################################################

class TENN_VectorDB():

        # Vector Database structure
        # database: {
        #     collection embed_db_text: {
        #      object1: {
        #       object_documents:{},
        #       object_embeddings:{},
        #       object_metadata:{
        #        {object_id: int,
        #         object_aid: uuid,
        #         object_url: str,
        #         object_tags: []}
        #        }
        #     },
        #      object2:{},
        #      object3:{}
        #     },
        #     collection embed_db_image: {},
        #     collection embed_db_audio: {},
        #     collection embed_db_video: {}
        # }

    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = True):
        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()        

        # Set the key properties
        self.db_url = None
        self.db_engine_type = None
        self.engine = None # Will be set in the connect() function
        self.verbose = passed_verbose
        self.engine: chromadb.Client = None

        # If the passed db url is none or empty, use the standard sql db path from the properties
        if passed_db_path is None or passed_db_path == "":
            self.db_url = self.properties.standard_vector_db_path
        elif not os.path.isdir(passed_db_path):
            print("TENN_VectorDB - Passed database path (" + passed_db_path + ") is not a valid path. Switching to standard VectorDB location.")
            self.db_url = self.properties.standard_vector_db_path
        else:
            self.db_url = os.path.abspath(passed_db_path)
        if self.verbose: print("TENN_VectorDB - Using database path " + self.db_url)

        # If the passed db engine is none or empty, use the standard sql db engine from the properties
        if passed_db_engine is None or passed_db_engine == "":
            self.db_engine_type = self.properties.standard_vector_db_engine
        elif passed_db_engine not in self.properties.allowed_engines:
            print("TENN_VectorDB - Unsupported database engine type (" + passed_db_engine + "). Switching to standard Vector database.")
            self.db_engine_type = self.properties.standard_vector_db_engine
        else:
            self.db_engine_type = passed_db_engine
        if self.verbose: print("TENN_VectorDB - Using database engine " + self.db_engine_type)

        # TODO Create support for cloud and other vector databases
            
    ##############################################################################################################################

    # Connect to the vector database and return the engine/client
    # def connect(self) -> chromadb.Client:

    #     # TODO Create support for cloud and other vector databases

    #     # We will force chromadb for now, but we need to DELETE THIS LATER
    #     if self.db_engine_type != self.properties.standard_vector_db_engine:
    #         print("TENN_VectorDB - Unsupported database engine type (" + self.db_engine_type + "). Switching to standard Vector database.")
    #         self.db_engine_type = self.properties.standard_vector_db_engine

    #     # Detect what engine type and connect accordingly

    #     if self.db_engine_type == "chromadb":

    #             # Initialize the settings for the vectorDB
    #             client_settings = chromadb.Settings(
    #                 chroma_db_impl="duckdb+parquet",
    #                 persist_directory=self.db_url,
    #                 anonymized_telemetry=False
    #             )

    #             # Create the engine based on db_type.
    #             try:
    #                 self.engine = chromadb.Client(settings=client_settings)
    #             except Exception as e:
    #                 if self.verbose: print("TENN_VectorDB - Connect error: " + str(e))
    #                 return None
                
    #             if self.verbose: print("TENN_VectorDB - Connected to the database.")
    #             return self.engine
    #     else:
    #             return None
     # TODO Create support for cloud and other vector databases
    def connect(self) -> chromadb.Client:
    # We will force chromadb for now, but we need to DELETE THIS LATER
        if self.db_engine_type != self.properties.standard_vector_db_engine:
            print("TENN_VectorDB - Unsupported database engine type (" + self.db_engine_type + "). Switching to standard Vector database.")
            self.db_engine_type = self.properties.standard_vector_db_engine

        # Detect what engine type and connect accordingly
        if self.db_engine_type == "chromadb":
            # Create the engine based on db_type.
            try:
                self.engine = chromadb.PersistentClient(path=self.db_url)
            except Exception as e:
                if self.verbose: print("TENN_VectorDB - Connect error: " + str(e))
                return None

            if self.verbose: print("TENN_VectorDB - Connected to the database.")
            return self.engine
        else:
            return None
                               
        # TODO - Add support for other vector databases here, other than chromadb

    ##############################################################################################################################
    # Function to return the db client/engine
    def get_client(self):
        return self.engine

    ##############################################################################################################################
    def get_collection(self, passed_model : str = "", passed_collection_name : str = ""):
        
        if passed_collection_name is None or passed_collection_name == "" or passed_model is None or passed_model == "":
            if self.verbose: print("TENN_VectorDB - Passed collection name or embedding type is empty.")
            return None

        # Infer the embedding function from the type of awareness
        # TODO - WE NEED TO REVISIT THIS AND USE THE RIGHT EMBEDDING FUNCTION FOR EACH TYPE OF EMBEDDINGSS, AND PREFERABLY USE LOCAL EMBEDDINGS ENGINES
        embedding_function_to_use = embedding_functions.OpenAIEmbeddingFunction(api_key = self.properties.openai_api_key, model_name = passed_model)

        self.connect()

        # Get the collection based on the collection_name and embedding function
        return self.get_or_create_collection(passed_collection_name = passed_collection_name, embedding_function = embedding_function_to_use)

    def get_or_create_collection(self, passed_collection_name: str = "", embedding_function: str = ""):
        if passed_collection_name is None or embedding_function == "":
            if self.verbose: print("TENN_VectorDB - Collection name is none or empty")
            return None

        # Try to get the collection
        try:
            collection = self.engine.get_collection(passed_collection_name, embedding_function)
        except Exception as e:
            if self.verbose: print("TENN_VectorDB - Error getting collection: " + str(e))
            collection = None

        # If the collection does not exist, create it
        if collection is None:
            try:
                collection = self.engine.create_collection(passed_collection_name,embedding_function = embedding_function)
                if self.verbose: print("TENN_VectorDB - Created new collection: " + passed_collection_name)
            except Exception as e:
                if self.verbose: print("TENN_VectorDB - Error creating collection: " + str(e))
                return None

        return collection

    ##############################################################################################################################

    # Function to return a list of all collections in the vectorDB

    def get_collections(self) -> list:
        return self.engine.list_collections() 
    
    ##############################################################################################################################

    # Function to return vectorstore

    def get_vectorstore(self,passed_collection_name: str = "", embedding_function_name: str = "") -> Chroma:
        Client=self.connect()
        embedding_function=OpenAIEmbeddings(openai_api_key=self.properties.openai_api_key ,model= embedding_function_name )
        vector_store = Chroma(
            client=Client,
            collection_name=passed_collection_name,
            embedding_function=embedding_function,
        )
        return vector_store