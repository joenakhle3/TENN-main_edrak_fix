import os
import sys

# Import the TENN utilities
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_config_ai import TENN_ConfigAI

# Import the TENN databases and objects

from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db    import TENN_EdrakDB, TENN_Awareness
from tenn_ai.fabric_ai.edrak.databases.tenn_object_db   import TENN_ObjectDB, TENN_Object
from tenn_ai.fabric_ai.edrak.databases.tenn_organize_db import TENN_OrganizeDB, TENN_Tag
from tenn_ai.fabric_ai.edrak.databases.tenn_input_db    import TENN_InputDB, TENN_Input, TENN_Input_Contents
from tenn_ai.fabric_ai.edrak.databases.tenn_embed_db    import TENN_EmbedDB

from tenn_ai.fabric_ai.edrak.databases.tenn_api_db      import TENN_ApiDB, TENN_Api
from tenn_ai.fabric_ai.edrak.databases.tenn_template_db import TENN_TemplateDB, TENN_Template
from tenn_ai.fabric_ai.edrak.databases.tenn_prompt_db   import TENN_PromptDB, TENN_Prompt
# from tenn_ai.fabric_ai.edrak.databases.tenn_intent_db import TENN_IntentDB, TENN_Intent

# Import SQLalchemy
from sqlalchemy import Engine, Table, Column
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from bson import ObjectId

#########################################################################################################

class TENN_EdrakAI():
    
    ######################################################################################################

    def __init__(self, passed_configAI: TENN_ConfigAI = None, passed_verbose: bool = False):
        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        # Set the needed variables
        self.configAI = passed_configAI
        self.verbose = passed_verbose

        # Set the needed databases
        self.edrakDB = TENN_EdrakDB()       # Manage the AID 
        # self.organizeDB = TENN_OrganizeDB()  # Manage the tags
        self.inputDB = TENN_InputDB()        # Manage the inputs
        self.embedDB = TENN_EmbedDB()        # Manage the embeddings
        self.objectDB =TENN_ObjectDB() 
        self.apiDB = TENN_ApiDB()            # Manage the APIs
        self.templateDB =TENN_TemplateDB()  # Manage the templates
        self.promptDB =TENN_PromptDB()      # Manage the prompts
#       self.intentDB: TENN_IntentDB()
#       self.fs: TENN_EdrakFS()

    ######################################################################################################

    # Function to create the core awareness for a given input
    # It receives the TENN_Input and TENN_Input_Contents from the TENN_InputAI class
    # It then creates awareness for the input, contents and chunks
    # Creates a TENN_Awareness object and store it in EdrakDB and generate an AID
    # Retrieve metadata from organizeAI
    # Store the full contents in objectDB
    # Store the chunks and embeds them in embedDB
    # Generate any additional awareness if needed (future)
    # It returns the awareness ID (AID)

    # TENN_Awareness structure is this
    # self.aid = passed_aid
    # self.url = passed_url
    # self.name = passed_name
    # self.description = passed_description
    # self.input_type = passed_input_type
    # self.content_type = passed_content_type
    # self.awareness_list = passed_awareness_list

    def create_or_update_core_awareness(self, passed_input: TENN_Input, passed_input_contents: TENN_Input_Contents) -> TENN_Awareness:

        # If the input or input_contents are None, return an error
        if passed_input is None or passed_input_contents is None:
            if self.verbose: print("TENN_EdrakAI - create_or_update_core_awareness - Error: Please specify an input and input contents.")
            return None

        awareness: TENN_Awareness = None

        # Check if the URL we received in the input already exists in the edrakDB, if so, let's update it
        existing_awareness: TENN_Awareness = self.edrakDB.get_awareness_for_url(passed_input.url)

        if existing_awareness is not None:
            print("TENN_EdrakAI - create_or_update_core_awareness - Awareness exists, updating awareness for " + passed_input.url)
            awareness = existing_awareness
        else:
            print(f"TENN_EdrakAI - create_or_update_core_awareness - Creating awareness for {passed_input.url}")
            awareness = TENN_Awareness()
            awareness.aid: str = self.utils.generate_aid()
            awareness.url: str = passed_input.url
            awareness.name: str = ""
            awareness.description: str = ""
            awareness.input_type: str = passed_input.input_type
            awareness.content_type: str = passed_input_contents.content_type
            awareness.awareness_list = "" # TODO store a json file with the awareness list

            # Add the "awareness_aid" to every dictionary within the metadatas list
            # for metadata_dict in passed_input_contents.metadatas:
            #     metadata_dict["awareness_aid"] = awareness.aid

            # Save the awareness object in TENN_EdrakDB
            awareness.aid = self.edrakDB.add_or_update_awareness(awareness)
            
        # Store the contents of the input in TENN_ObjectDB in the relevant collection
        object = TENN_Object()
        object.aid = awareness.aid
        object.content_type = passed_input_contents.content_type
        object.contents = passed_input_contents.full_content

        object_id: ObjectId = self.objectDB.add_object_core(passed_object=object)

        # Create embeddings in TENN_EmbedDB for the input content
        self.embedDB.create_embeddings(passed_awareness=awareness,passed_input=passed_input,passed_input_contents=passed_input_contents)

        return awareness

    ######################################################################################################

    # def delete_awareness(self, passed_aid: str = "") -> bool:

    #     aid = passed_aid    
    #     # Set the edrakDB path
    #     edrakDB = TENN_EdrakDB(self.edrakDB_path)
    #     print ("TENN_Ingest - delete_awareness - The edrakDB path is: " + self.edrakDB_path)
    #     print ("TENN_Ingest - delete_awareness - Deleting awareness for url: " + url)

    #     # Get the multimodal adapter for the url so we can work with it
    #     adapter = TENN_Multimodal_Adapter(url)
    #     if url == None or url == "" or adapter.type == "UNKNOWN" or adapter.type == "FOLDER":
    #         print("TENN_Ingest - delete_awareness - This is not a valid or known file type. Skipping it.")
    #         return

    #     # If the awareness already exists in the edrakDB, delete the awareness
    #     if edrakDB.awareness_exists_for_url(url, adapter.awareness_type):
    #         print(f"TENN_Ingest - delete_awareness - Knowledge exists for {url}. Deleting.")
    #         edrakDB.delete_awareness_for_url(url, adapter.awareness_type)
    #     else:
    #         print(f"TENN_Ingest - delete_awareness - Knowledge does not exist for {url}. Skipping it.")
    #         return

    #     edrakDB.client.persist()
    #     print(f"TENN_Ingest - delete_awareness - Successfully deleted awareness for {url}")

    #     # TODO Create all types of awareness
    #     # Return the awareness ID (AID)
    #     return aid
    
    ######################################################################################################