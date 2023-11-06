# imports for the Generate class

import os
import sys
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document

# Import TENN classes
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db import TENN_EdrakDB

##################################################################################################################################

# The Generate class allows interaction with generative services of TENN Fabric

class TENN_GenerateAI:
    def __init__(self, passed_edrakDB_path: str, passed_verbose: bool = False):

        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.verbose = passed_verbose

        # if passed_embeddings is None then use the default embeddings
        if passed_edrakDB_path == "" or passed_edrakDB_path is None:
            print("TENN_Generate - Invalid edrakDB path!")
            sys.exit(1)
        else:
            self.edrakDB_path = passed_edrakDB_path
            # do your stuff here

    
    ##############################################################################################################################

    # Function chat that takes an edrakdb_path, a chat history and a prompt, and returns an AI answer using openAI GPT API

    def chat_simple_qna(self, passed_prompt: str = None, 
                        passed_temperature: float = 0, 
                        passed_edrakdb_path: str = None, 
                        passed_chat_history: str = None,
                        passed_system_prompt: str = None) -> str:

        # Avoid invoking the LLM if the prompt is empty or edrakDB_path is invalid
        if passed_prompt == "" or passed_prompt is None:
            return ""

        # We need to use the edrakDB and create a retriever with openAI
        return "the answer is 10"

    ##############################################################################################################################