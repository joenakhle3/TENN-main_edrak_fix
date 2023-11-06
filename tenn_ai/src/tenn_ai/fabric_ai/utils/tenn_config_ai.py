import os
import sys
import json

from typing import List
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils

# Class which has all the configuration properties needed from engageAI which will be used by all other classes

class TENN_ConfigAI:
    def __init__(self):
            # "username": "",
            # "edrakFS_folder": "",
            # "edrakDB_path": "",
            # "edrakFS_monitor_enabled": False,
            # "inputAI_template": "",
            # "edrakDB_collections_selected": [],
            # "edrakDB_urls_selected": [],
            # "edrakDB_metadata_selected": [],
            # ADD edrakDB_filter_string ################################################################
            # "generateAI_chat_history": "",
            # "generateAI_prompt": "",
            # "generateAI_system_prompt": "",
            # "generateAI_temperature": 0,
            # "generateaAI_k": 3,
            # "generateAI_distance_threshold": 0.5,
            # "generateAI_plugins_selected": [],
            # "generateAI_response": [],
            # "outputAI_template": "",
            # "multiAI_model_selected": "",
            # "multiAI_intent": [],
        
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        # Initialize a JSON object with all the properties
        self.clear_configuration()

    ##############################################################################################################################
    # Print the configuration in a nice formatted key: value format

    def get_printable_configuration(self):
        return json.dumps(self.configuration, indent=4)


    ##############################################################################################################################
    # The clear_<propertyname> functions

    def clear_configuration(self):
        self.configuration : json = {
            "username": "",
            "edrakFS_folder": "",
            "edrakDB_path": "",
            "edrakFS_monitor_enabled": False,
            "inputAI_template": "",
            "edrakDB_collections_selected": [],
            "edrakDB_urls_selected": [],
            "edrakDB_metadata_selected": [],
            "generateAI_chat_history": "",
            "generateAI_prompt": "",
            "generateAI_system_prompt": "",
            "generateAI_temperature": 0,
            "generateaAI_k": 3,
            "generateAI_distance_threshold": 0.5,
            "generateAI_plugins_selected": [],
            "generateAI_response": [],
            "outputAI_template": "",
            "multiAI_model_selected": "",
            "multiAI_intent": [],
        } 

    def clear_username(self):
        self.configuration["username"] = ""

    def clear_edrakFS_folder(self):
        self.configuration["edrakFS_folder"] = ""

    def clear_edrakDB_path(self):
        self.configuration["edrakDB_path"] = ""

    def clear_edrakFS_monitor_enabled(self):
        self.configuration["edrakFS_monitor_enabled"] = False

    def clear_inputAI_template(self):
        self.configuration["inputAI_template"] = ""

    def clear_edrakDB_collections_selected(self):
        self.configuration["edrakDB_collections_selected"] = []

    def clear_edrakDB_urls_selected(self):
        self.configuration["edrakDB_urls_selected"] = []

    def clear_edrakDB_metadata_selected(self):
        self.configuration["edrakDB_metadata_selected"] = []

    def clear_generateAI_chat_history(self):
        self.configuration["generateAI_chat_history"] = ""

    def clear_generateAI_prompt(self):
        self.configuration["generateAI_prompt"] = ""

    def clear_generateAI_system_prompt(self):
        self.configuration["generateAI_system_prompt"] = ""

    def clear_generateAI_temperature(self):
        self.configuration["generateAI_temperature"] = 0

    def clear_generateaAI_k(self):
        self.configuration["generateaAI_k"] = 3
    
    def clear_generateAI_distance_threshold(self):
        self.configuration["generateAI_distance_threshold"] = 0.5

    def clear_generateAI_plugins_selected(self):
        self.configuration["generateAI_plugins_selected"] = []

    def clear_generateAI_response(self):
        self.configuration["generateAI_response"] = []

    def clear_outputAI_template(self):
        self.configuration["outputAI_template"] = ""

    def clear_multiAI_model_selected(self):
        self.configuration["multiAI_model_selected"] = ""
    
    def clear_multiAI_intent(self):
        self.configuration["multiAI_intent"] = []

    ##############################################################################################################################
    # The set_<propertyname> functions

    def set_configuration(self, passed_configuration: json):
        self.configuration = passed_configuration

    def set_username(self, passed_username: str):
        self.configuration["username"] = passed_username

    def set_edrakFS_folder(self, passed_edrakFS_folder: str):
        self.configuration["edrakFS_folder"] = passed_edrakFS_folder

    def set_edrakDB_path(self, passed_edrakDB_path: str):
        self.configuration["edrakDB_path"] = passed_edrakDB_path

    def set_edrakFS_monitor_enabled(self, passed_edrakFS_monitor_enabled: bool):
        self.configuration["edrakFS_monitor_enabled"] = passed_edrakFS_monitor_enabled

    def set_inputAI_template(self, passed_inputAI_template: str):
        self.configuration["inputAI_template"] = passed_inputAI_template

    def set_edrakDB_collections_selected(self, passed_edrakDB_collections_selected: List[str]):
        self.configuration["edrakDB_collections_selected"] = passed_edrakDB_collections_selected

    def set_edrakDB_urls_selected(self, passed_edrakDB_urls_selected: List[str]):
        self.configuration["edrakDB_urls_selected"] = passed_edrakDB_urls_selected
    
    def set_edrakDB_metadata_selected(self, passed_edrakDB_metadata_selected: List[str]):
        self.configuration["edrakDB_metadata_selected"] = passed_edrakDB_metadata_selected
    
    def set_generateAI_chat_history(self, passed_generateAI_chat_history: str):
        self.configuration["generateAI_chat_history"] = passed_generateAI_chat_history
    
    def set_generateAI_prompt(self, passed_generateAI_prompt: str):
        self.configuration["generateAI_prompt"] = passed_generateAI_prompt
    
    def set_generateAI_system_prompt(self, passed_generateAI_system_prompt: str):
        self.configuration["generateAI_system_prompt"] = passed_generateAI_system_prompt
    
    def set_generateAI_temperature(self, passed_generateAI_temperature: float):
        self.configuration["generateAI_temperature"] = passed_generateAI_temperature
    
    def set_generateaAI_k(self, passed_generateaAI_k: int):
        self.configuration["generateaAI_k"] = passed_generateaAI_k
    
    def set_generateAI_distance_threshold(self, passed_generateAI_distance_threshold: float):
        self.configuration["generateAI_distance_threshold"] = passed_generateAI_distance_threshold
    
    def set_generateAI_plugins_selected(self, passed_generateAI_plugins_selected: List[str]):
        self.configuration["generateAI_plugins_selected"] = passed_generateAI_plugins_selected
    
    def set_generateAI_response(self, passed_generateAI_response: List[str]):
        self.configuration["generateAI_response"] = passed_generateAI_response
    
    def set_outputAI_template(self, passed_outputAI_template: str):
        self.configuration["outputAI_template"] = passed_outputAI_template
    
    def set_multiAI_model_selected(self, passed_multiAI_model_selected: str):
        self.configuration["multiAI_model_selected"] = passed_multiAI_model_selected
    
    def set_multiAI_intent(self, passed_multiAI_intent: List[str]):
        self.configuration["multiAI_intent"] = passed_multiAI_intent
    
    ##############################################################################################################################
    # The get_<propertyname> functions

    def get_configuration(self) -> json:
        return self.configuration

    def get_username(self) -> str:
        return self.configuration["username"]
    
    def get_edrakFS_folder(self) -> str:
        return self.configuration["edrakFS_folder"]
    
    def get_edrakDB_path(self) -> str:
        return self.configuration["edrakDB_path"]
    
    def get_edrakFS_monitor_enabled(self) -> bool:
        return self.configuration["edrakFS_monitor_enabled"]
    
    def get_inputAI_template(self) -> str:
        return self.configuration["inputAI_template"]
    
    def get_edrakDB_collections_selected(self) -> List[str]:
        return self.configuration["edrakDB_collections_selected"]
    
    def get_edrakDB_urls_selected(self) -> List[str]:
        return self.configuration["edrakDB_urls_selected"]
    
    def get_edrakDB_metadata_selected(self) -> List[str]:
        return self.configuration["edrakDB_metadata_selected"]
    
    def get_generateAI_chat_history(self) -> str:
        return self.configuration["generateAI_chat_history"]
    
    def get_generateAI_prompt(self) -> str:
        return self.configuration["generateAI_prompt"]
    
    def get_generateAI_system_prompt(self) -> str:
        return self.configuration["generateAI_system_prompt"]
    
    def get_generateAI_temperature(self) -> float:
        return self.configuration["generateAI_temperature"]
    
    def get_generateaAI_k(self) -> int:
        return self.configuration["generateaAI_k"]
    
    def get_generateAI_distance_threshold(self) -> float:
        return self.configuration["generateAI_distance_threshold"]
        
    def get_generateAI_plugins_selected(self) -> List[str]:
        return self.configuration["generateAI_plugins_selected"]
    
    def get_generateAI_response(self) -> List[str]:
        return self.configuration["generateAI_response"]
    
    def get_outputAI_template(self) -> str:
        return self.configuration["outputAI_template"]
    
    def get_multiAI_model_selected(self) -> str:
        return self.configuration["multiAI_model_selected"]
    
    def get_multiAI_intent(self) -> List[str]:
        return self.configuration["multiAI_intent"]
