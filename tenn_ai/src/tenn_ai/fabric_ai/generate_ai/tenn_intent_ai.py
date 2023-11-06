# imports for the Generate class

import os
import sys
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import logging

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

# Import Camel and ChatChain
from tenn_ai.fabric_ai.generate_ai.camel.typing import ModelType
from tenn_ai.fabric_ai.generate_ai.chatdev.chat_chain import ChatChain

root = os.path.dirname(__file__)
sys.path.append(root)

##################################################################################################################################

# The Generate class allows interaction with generative services of TENN Fabric

class TENN_IntentAI:
    def __init__(self, passed_config_folder: str = "TENN", passed_org: str = "TENN", passed_task: str = "", passed_name = "TENN", passed_model = "GPT_3_5_TURBO", passed_verbose: bool = False):

        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.verbose = passed_verbose

        # Set the configuration
        self.config_folder = passed_config_folder
        self.org = passed_org
        self.task = passed_task
        self.name = passed_name

        # Set the model
        self.config_path, self.config_phase_path, self.config_role_path = self.get_intent_config(self.config_folder)
        self.model_types = {'GPT_3_5_TURBO': ModelType.GPT_3_5_TURBO, 'GPT_4': ModelType.GPT_4, 'GPT_4_32K': ModelType.GPT_4_32k}
        self.model = self.model_types[passed_model]
    
    ##############################################################################################################################

    # Get the configuration for ChatChain from the appropriate company folder

    def get_intent_config(self, passed_company: str = "TENN") -> List[str]:
        """
        return configuration json files for ChatChain
        user can customize only parts of configuration json files, other files will be left for default
        Args:
            company: customized configuration name under CompanyConfig/

        Returns:
            path to three configuration jsons: [config_path, config_phase_path, config_role_path]
        """
        config_dir = os.path.join(root, "IntentConfig", passed_company)
        if self.verbose: print(config_dir)
        default_config_dir = os.path.join(root, "IntentConfig", "TENN")

        config_files = [
            "ChatChainConfig.json",
            "PhaseConfig.json",
            "RoleConfig.json"
        ]

        config_paths = []

        for config_file in config_files:
            company_config_path = os.path.join(config_dir, config_file)
            default_config_path = os.path.join(default_config_dir, config_file)

            if os.path.exists(company_config_path):
                config_paths.append(company_config_path)
            else:
                config_paths.append(default_config_path)

        return tuple(config_paths)

    ##############################################################################################################################

    def run(self):
        # ----------------------------------------
        #          Init ChatChain
        # ----------------------------------------
        chat_chain = ChatChain( config_path = self.config_path,
                                config_phase_path = self.config_phase_path,
                                config_role_path = self.config_role_path,
                                task_prompt = self.task,
                                project_name = self.name,
                                org_name = self.org,
                                model_type = self.model
                              )

        # ----------------------------------------
        #          Init Log
        # ----------------------------------------
        logging.basicConfig(filename=chat_chain.log_filepath, 
                            level=logging.INFO,
                            format='[%(asctime)s %(levelname)s] %(message)s',
                            datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8"
                            )

        # ----------------------------------------
        #          Pre Processing
        # ----------------------------------------

        chat_chain.pre_processing()

        # ----------------------------------------
        #          Personnel Recruitment
        # ----------------------------------------

        chat_chain.make_recruitment()

        # ----------------------------------------
        #          Chat Chain
        # ----------------------------------------

        chat_chain.execute_chain()

        # ----------------------------------------
        #          Post Processing
        # ----------------------------------------

        chat_chain.post_processing()
