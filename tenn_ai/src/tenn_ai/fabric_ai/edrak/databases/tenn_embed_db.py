import os
import sys
import json
import datetime
import time
import uuid

from typing import List
from langchain.chains import RetrievalQA
import langchain
# from langchain import vectorstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import chroma

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.stores.tenn_vector_db import TENN_VectorDB
from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db    import TENN_EdrakDB, TENN_Awareness
from tenn_ai.fabric_ai.edrak.databases.tenn_input_db    import TENN_InputDB, TENN_Input, TENN_Input_Contents
from tenn_ai.fabric_ai.edrak.tenn_edrak_ai   import TENN_InputDB, TENN_Input, TENN_Input_Contents



from typing import List, Dict, Optional
# from chromadb import VectorStoreRetriever


# Class that extends TENN_SqlDB to create all needed functions of the Embeddings DB

# #########################################################################################################
class TENN_EmbedDB(TENN_VectorDB):

    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = True):
        super().__init__(passed_db_path, passed_db_engine, passed_verbose)
        self.utils=TENN_Utils()
        self.properties=TENN_Properties()
        self.verbose = passed_verbose

    ############
    def create_embeddings(self,passed_awareness: TENN_Awareness, passed_input:TENN_Input, passed_input_contents: TENN_Input_Contents):
        
        # Check if the passed awareness is None
        if passed_awareness is None or passed_input is None or passed_input_contents is None :
            if self.verbose: print("TENN_EmbedDB - The passed awareness or input data is invalid.")
            return None
        try:
            properties=TENN_Properties()
            passed_content_type = passed_input_contents.content_type

            passed_collection_name = self.utils.get_core_collection_name_for_content_type(passed_content_type)
            # passed_model = self.utils.get_embeddings_model_for_collection(passed_collection_name)
            passed_model=properties.collections_and_embeddings_models[passed_collection_name]
            # collection =  super().get_collection(passed_collection_name=passed_collection_name, passed_embeddings_model=passed_model)
            collection =  super().get_collection(passed_model , passed_collection_name)
            ids=passed_input_contents.ids
            documents=passed_input_contents.documents
            metadatas=passed_input_contents.metadatas
            # Add the documents, IDs, metadata, and aid to the collection

            collection.add(ids=ids,documents=documents,metadatas=metadatas)
            # metadatas=passed_input_contents.metadatas,
            # Persist the co llection
            # collection.persist()

            # Return the ChromaDB collection
            return collection
        except:
            if self.verbose: print("TENN_EmbedDB - Error adding embeddings to the database.")
            return None


            # Embed documents, IDs, and metadatas separately using the parameters
    # def get_collection(self,passed_model,passed_collection_name):
    #     collection =  super().get_collection(passed_model , passed_collection_name )
    #     return collection



    ##############################################################################################################################

    def get_collection(self, passed_collection_name: str = "CORE_TEXT"):

        if (passed_collection_name is None) or (passed_collection_name == "") or (passed_collection_name not in self.properties.collections_and_embeddings_models.keys()):
            if self.verbose: print("TENN_EmbedDB - get_collection - Passed collection name (" + passed_collection_name + ") is not valid. ")
            return None
        
        model = passed_model = self.utils.get_embeddings_model_for_collection[passed_collection_name]

        return super().get_collection(passed_collection_name=passed_collection_name, passed_embeddings_model=model)

    ##############################################################################################################################

    def get_aids_in_collection(self, passed_collection_name : str = "") -> list:
            
            # Get the collection
            collection = self.get_collection(passed_collection_name = passed_collection_name) 
            
            # Get all the documents in the collection
            result = collection.get(include=["aid"])
            
            return result

    ##############################################################################################################################

    def get_urls_in_collection(self, passed_collection_name : str = "") -> list:
            
            # Get the collection
            collection = self.get_collection(passed_collection_name = passed_collection_name) 
            
            # Get all the documents in the collection
            result = collection.get(include=["url"])
            
            return result
    
    ##############################################################################################################################

    # Function to return a list of all urls in the vectorDB across all collections

    def get_all_urls(self) -> list:
            
            # Get all the collections
            all_collections = self.get_collections()
            
            # Get the urls from all the collections
            all_urls = []
            for collection in all_collections:
                all_urls.extend(self.get_urls_in_collection(collection.name))
            
            return all_urls

    ##############################################################################################################################

    # Function to check if awareness exists for a URL in the vectorDB
    # TODO - WE NEED TO IMPROVE THIS TO CHECK FOR FILE CREATION DATE AND TIME, AND NOT JUST THE URL

    def embeddings_exists_for_url(self, passed_url : str = None, passed_collection_name : str = None) -> bool:

        # get existing ids, and discard doc if any common id exist.
        collection = self.get_collection(passed_collection_name=passed_collection_name)
        existing_docs = collection.get(where={"url": passed_url})
        return False if len(existing_docs)==0 else True
    
    ##############################################################################################################################
    # Function to delete all awareness for a URL from the vectorDB, for a certain awareness type or inside a specific collection
    def delete_embeddings_for_aid(self, aid: str):
        if self.verbose:  # Check if verbose mode is enabled
            print("TENN_EmbedDB - delete_embeddings_for_aid - Deleting embeddings for awareness id (aid):", aid)

        # Iterate through all collections and search for embeddings associated with the provided awareness id (aid).
        for collection_name in super().get_all_collections():
            collection = self.get_collection(passed_collection_name=collection_name)
            existing_docs = collection.get(where={"aid": aid})
            existing_ids = list(existing_docs["ids"])

            if len(existing_ids) > 0:
                if self.verbose:  # Check if verbose mode is enabled
                    print("TENN_EmbedDB - delete_embeddings_for_aid - Embeddings exist in the vectorDB for this awareness id (aid). Deleting.")
                collection.delete(ids=existing_ids)
                self.engine.persist()
            else:
                if self.verbose:  # Check if verbose mode is enabled
                    print("TENN_EmbedDB - delete_embeddings_for_aid - No embeddings found for this awareness id (aid) in collection:", collection_name, ". Skipping.")

    ##############################################################################################################################

    def delete_embeddings_for_aid_and_url(self, aid: str, url: str):
        if self.verbose:  # Check if verbose mode is enabled
            print("TENN_EmbedDB - delete_embeddings_for_aid_and_url - Deleting embeddings for awareness id (aid):", aid, "and URL:", url)

        # Iterate through all collections and search for embeddings associated with the provided "aid" and URL.
        for collection_name in super().get_all_collections():
            collection = self.get_collection(collection_name)
            existing_docs = collection.get(where={"aid": aid, "url": url})
            existing_ids = list(existing_docs["ids"])

            if len(existing_ids) > 0:
                if self.verbose:  # Check if verbose mode is enabled
                    print("TENN_EmbedDB - delete_embeddings_for_aid_and_url - Embeddings exist in the vectorDB for this awareness id (aid) and URL. Deleting in collection:", collection_name)
                collection.delete(ids=existing_ids)
                self.engine.persist()
            else:
                if self.verbose:  # Check if verbose mode is enabled
                    print("TENN_EmbedDB - delete_embeddings_for_aid_and_url - No embeddings found for this awareness id (aid) and URL in collection:", collection_name, ". Skipping.")


 ##############################################################################################################################

    def get_tags(self, aid: str) -> List[str]:
        # Search for the document in the database using the provided AID
        collection = self.get_collection()
        existing_docs = collection.get(where={"aid": aid})
        
        # Check if the document with the given AID exists and contains tags
        if existing_docs and "tags" in existing_docs:
            return existing_docs["tags"]
        else:
            return []


    ##############################################################################################################################

    def get_metadata(self, aid: str) -> Dict:
        # Initialize an empty dictionary to store metadata
        metadata = {}
        
        if self.verbose:  # Check if verbose mode is enabled
            print("TENN_EmbedDB - get_metadata - Retrieving metadata for awareness id (aid):", aid)

        # Iterate through all collections and search for metadata associated with the provided "aid".
        for collection_name in super().get_all_collections():
            collection = self.get_collection(collection_name)
            existing_docs = collection.get(where={"aid": aid})
            
            # Check if the document with the given AID exists and contains metadata
            if existing_docs and "metadata" in existing_docs:
                # Merge the metadata from this collection with the existing metadata dictionary
                metadata.update(existing_docs["metadata"])
        
        return metadata

    ##############################################################################################################################

    def aid_exists(self, aid: str) -> bool:
        # Search for the AID in the database
        collection = self.get_collection()
        existing_docs = collection.get(where={"aid": aid})
        return bool(existing_docs)

    ##############################################################################################################################

    def url_exists(self, url: str) -> bool:
   
        # Search for the URL in the database
        collection = self.get_collection()
        existing_docs = collection.get(where={"url": url})
        return bool(existing_docs)

    ##############################################################################################################################

    def embeddings_exist(self, aid_or_url: str) -> bool:
        # Check if it's an AID or URL
        if len(aid_or_url) == 36 and '-' in aid_or_url:
            # It's an AID, so search for it in the database
            collection = self.get_collection()
            existing_docs = collection.get(where={"aid": aid_or_url})
        else:
            # It's a URL, so search for it in the database
            collection = self.get_collection()
            existing_docs = collection.get(where={"url": aid_or_url})
        
        return bool(existing_docs)
    
    ##############################################################################################################################

    def update_metadata_by_aid(self, aid: str, metadata: Dict) -> bool:
        # Initialize a flag to track whether metadata was updated
        metadata_updated = False

        # Iterate through all collections and search for documents with the given "aid"
        for collection_name in super().get_all_collections():
            collection = self.get_collection(collection_name)
            existing_docs = collection.get(where={"aid": aid})

            if existing_docs:
                # Metadata exists for this "aid" in this collection
                existing_metadata = existing_docs.get("metadata", {})
                existing_metadata.update(metadata)
                existing_docs["metadata"] = existing_metadata
                collection.update(existing_docs)
                metadata_updated = True  # Set the flag to True indicating metadata was updated

        # If metadata was updated in at least one collection, persist the database and return True; otherwise, return False
        if metadata_updated:
            self.engine.persist()  # Persist the database to save the changes
        return metadata_updated

##############################################################################################################################

    def update_metadata_by_awareness(self, awareness_type: str, aid: str, collection_name: str, metadata: Dict) -> bool:
        # Initialize a flag to track whether metadata was updated
        metadata_updated = False

        # Get the specified collection
        collection = self.get_collection(awareness_type, collection_name)
        
        # Search for documents with the given "aid" in the specified collection
        existing_docs = collection.get(where={"aid": aid})

        if existing_docs:
            # Metadata exists for this "aid" in this collection
            existing_metadata = existing_docs.get("metadata", {})
            existing_metadata.update(metadata)
            existing_docs["metadata"] = existing_metadata
            collection.update(existing_docs)
            metadata_updated = True  # Set the flag to True indicating metadata was updated

            # Persist the database to save the changes
            self.engine.persist()

        return metadata_updated

    ##############################################################################################################################

    def delete_text_embeddings(self, aid_or_url: str):
        if self.verbose:  # Check if verbose mode is enabled
            if len(aid_or_url) == 36 and '-' in aid_or_url:
                print("TENN_EmbedDB - delete_text_embeddings - Deleting text embeddings for AID:", aid_or_url)
            else:
                print("TENN_EmbedDB - delete_text_embeddings - Deleting text embeddings for URL:", aid_or_url)

        # Check if it's an AID or URL
        if len(aid_or_url) == 36 and '-' in aid_or_url:
            # It's an AID, so search for it in the database and delete text embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"aid": aid_or_url})
        else:
            # It's a URL, so search for it in the database and delete text embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"url": aid_or_url})
        
        if existing_docs:
            # Check if the document has text embeddings
            if "text_embeddings" in existing_docs:
                # Assuming text_embeddings is a list of text embeddings
                text_embeddings = existing_docs["text_embeddings"]
                text_embeddings.clear()
                collection.update(existing_docs)
            else:
                if self.verbose:  # Check if verbose mode is enabled
                    print("TENN_EmbedDB - delete_text_embeddings - No text embeddings found for this document.")
        else:
            if self.verbose:  # Check if verbose mode is enabled
                print("TENN_EmbedDB - delete_text_embeddings - Document not found in the collection.")

    ##############################################################################################################################

    def create_image_embeddings(self, aid: str):
     
        # Create image embeddings for the given AID (assuming image embeddings)
        collection = self.get_collection()
        # CELINE CODE

    ##############################################################################################################################

    def delete_image_embeddings(self, aid_or_url: str):
     
        # Check if it's an AID or URL
        if len(aid_or_url) == 36 and '-' in aid_or_url:
            # It's an AID, so search for it in the database and delete image embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"aid": aid_or_url})
        else:
            # It's a URL, so search for it in the database and delete image embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"url": aid_or_url})
        
        if existing_docs:
            for doc in existing_docs:
                if 'embeddings' in doc:
                    # Assuming 'embeddings' is the key for storing image embeddings in your data structure
                    del doc['embeddings']
            
            # Now, update the documents in the database or data structure
            collection = self.get_collection()  # Assuming you have a method to get the collection
            for doc in existing_docs:
                collection.update(doc, doc_ids=[doc.doc_id])

    ##############################################################################################################################
    def delete_all_embeddings(self, aid_or_url: str):
       
        # Check if it's an AID or URL
        if len(aid_or_url) == 36 and '-' in aid_or_url:
            # It's an AID, so search for it in the database and delete all embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"aid": aid_or_url})
        else:
            # It's a URL, so search for it in the database and delete all embeddings
            collection = self.get_collection()
            existing_docs = collection.get(where={"url": aid_or_url})
        
        if existing_docs:
            for doc in existing_docs:
                if 'embeddings' in doc:
                    # Assuming 'embeddings' is the key for storing embeddings in your data structure
                    del doc['embeddings']
            # Now, update the documents in the database or data structure
            collection = self.get_collection()  # Assuming you have a method to get the collection
            for doc in existing_docs:
                collection.update(doc, doc_ids=[doc.doc_id])

    ##############################################################################################################################

class TENN_filter:
  def __init__(self, passed_filter: list= None):
    # if passed_embeddings is None then use the default embeddings
    if passed_filter is None:
      self.sources = None
    else:
      self.sources = passed_filter

  def organize_filter(self):
    if self.sources is None:
      self.filter = None
      return self.filter

    if len(self.sources) == 1:
      self.filter = {"source": self.sources[0]}
      return self.filter

    else:
      or_conditions = [{'source': {'$eq': url}} for url in self.sources]
      self.filter = {'$or': or_conditions}
      return self.filter
# if __name__ == "__main__":
#    filter= TENN_filter(["https://www.youtube.com/watch?v=-B0dNAednJ8","https://www.youtube.com/watch?v=-B0dNAednJ8","https://www.youtube.com/watch?v=-B0dNAednJ8","https://www.youtube.com/watch?v=-B0dNAednJ8","https://www.youtube.com/watch?v=-B0dNAednJ8"]).organize_filter()
#    print(filter)

#   def retriever(self):
#     # Create and return a retriever based on chromadb's AsRetriever function
#     # Use the filter created by the organize_filter() method to filter the results.
#     retriever = self.vectorstore.as_retriever(search_kwargs={'filter': self.filter, 'k': self.k_value})
#     return retriever


        # TODO understand the VectorStoreRetriever from chromaDB and insert it here from the super() class


    ##############################################################################################################################

    # Function to return a list of urls in a certain collection in the vectorDB
    # https://docs.trychroma.com/reference/Collection
    # def get(ids: Optional[OneOrMany[ID]] = None,
    #         where: Optional[Where] = None,
    #         limit: Optional[int] = None,
    #         offset: Optional[int] = None,
    #         where_document: Optional[WhereDocument] = None,
    #         include: Include = ["metadatas", "documents"]) -> GetResult
    