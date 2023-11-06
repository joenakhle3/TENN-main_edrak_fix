import os
import sys

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_config_ai import TENN_ConfigAI

from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db import TENN_EdrakDB
from tenn_ai.fabric_ai.edrak.databases.tenn_embed_db import TENN_EmbedDB
from tenn_ai.fabric_ai.edrak.databases.tenn_template_db import TENN_TemplateDB, TENN_Template

# Import SQLalchemy
from sqlalchemy import Engine, Table, Column
from sqlalchemy import Integer, String, CHAR, DateTime, Boolean, Float, Text, LargeBinary, UUID
from sqlalchemy import ForeignKey, UniqueConstraint, Index, MetaData
from sqlalchemy.orm import mapper, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

#########################################################################################################

class TENN_TemplateAI():

    # #########################################################################################################

    def __init__(self, passed_configAI: TENN_ConfigAI):

        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()

        # Get the configAI object
        # TEAM TODO - Check if passed_configai is None, and if so, create a new configai object
        self.configAI = passed_configAI
        self.edrak_path = self.configAI.get_edrakDB_path()
        
        # Get the Organize DB
        self.vectorDB = TENN_EmbedDB(passed_db_path = self.edrak_path)
        self.templateDB = TENN_TemplateDB(passed_db_path = self.edrak_path)

        print ("TENN_TemplateAI - Loaded awareness DB with path " + self.edrak_path)

        # TODO TEAM - We need to get the collection based on the type of awareness selected by the user

