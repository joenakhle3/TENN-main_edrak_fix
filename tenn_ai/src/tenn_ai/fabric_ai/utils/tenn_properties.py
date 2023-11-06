import os
import urllib.parse
from pathlib import Path

from pydantic import BaseModel

##############################################################################################################################

# Environment variables
# OpenAI

os.environ["OPENAI_API_KEY"] = "REPLACE WITH YOUR OPENAI API KEY" ## REPLACE THIS
os.environ["TOKENIZERS_PARALLELISM"] = "False"

# Cohere
os.environ["COHERE_API_KEY"] = "j3TduAZfnNzc2195PFKjiz0vKSdJ5arNOoR4Nitn" ## REPLACE THIS

# AI21
os.environ["AI21_API_KEY"]   = "nd3vut08jQugp9byQItwZJYlnNxx2Ee4"   ## REPLACE THIS

# Google AI
os.environ["VERTEXAI_PROJECT"] = "tenn-vertex"
os.environ["VERTEXAI_LOCATION"] = "europe-west2"

# Azure AI
os.environ["AZURE_API_KEY"] = "INSERT AZURE API KEY HERE"
os.environ["AZURE_API_BASE"] = "https://openai-gpt-4-test-v-1.openai.azure.com/"
os.environ["AZURE_API_VERSION"] = "2023-05-15"

# SafeAI JWT
os.environ["JWT_SECRET"] = "~80.~{:dj#b.vK*lR.~HLzHMX?wkcWM?Ah#i$L9{c[!FMjxtc)H4a9>E?lXJ:ZHl"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_TIMEOUT"] = "3600"

##############################################################################################################################

class TENN_Properties():
    
    # Initialize the class variables
    def __init__(self):
        
        #################################################################################################################################
        # openAI API key
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.cohere_api_key = os.environ["COHERE_API_KEY"]
        self.ai21_api_key   = os.environ["AI21_API_KEY"]

        #################################################################################################################################
        # InputAI Properties
        # The list of extensions to ignore when ingesting files
        self.ignored_extensions = [".npy", ".DS_Store", ".gitkeep", ".gitignore", ".git", ".ipynb_checkpoints", ".pyc", ".py", ".pkl", ".tmp", ".faiss"]
        
        # The list of input types we know how to ingest
        self.input_types = ["FILE", "URL", "API", "STREAM"]

        #################################################################################################################################
        # Edrak Properties

        # list of embeddings models we will use for each collection/awareness
        self.awareness_types_and_collections = {"TEXT.EXTRACTED_TEXT": "CORE_TEXT",
                                                "TEXT.EXTRACTED_SUMMARY": "GEN_SUMMARY",
                                                "IMAGE.EXTRACTED_OCR_TEXT": "CORE_TEXT",
                                                "IMAGE.EXTRACTED_BINARY": "CORE_IMAGE",
                                                "IMAGE.GENERATED_SUMMARY": "GEN_SUMMARY",
                                                "VIDEO.EXTRACTEDـVIDEOـTRANSCRIPT": "CORE_TEXT",
                                                "VIDEO.EXTRACTED_BINARY": "CORE_VIDEO",
                                                "AUDIO.EXTRACTED_AUDIO_TRANSCRIPT": "CORE_TEXT",
                                                "AUDIO.EXTRACTED_BINARY": "CORE_AUDIO",
                                                "DATA.EXTRACTED_DATA": "CORE_DATA",
                                                "CODE.EXTRACTED_CODE": "CORE_CODE",
                                                "OBJECT.EXTRACTED_OBJECT": "CORE_OBJECT",
                                                "JSON.EXTRACTED_OBJECT": "CORE_OBJECT",
                                                "": "GEN_TEXT", 
                                                "": "GEN_SUMMARY",
                                                "": "GEN_TEMPLATE",
                                                "": "GEN_DATA",
                                                "": "GEN_CODE",
                                                "": "GEN_OBJECT",
                                                "": "GEN_IMAGE",
                                                "": "GEN_VIDEO",
                                                "": "GEN_AUDIO"}

        # list of embeddings models we will use for each collection/awareness
        self.collections_and_embeddings_models = {"CORE_TEXT": "text-embedding-ada-002",
                                                  "GEN_TEXT": "text-embedding-ada-002", 
                                                  "GEN_SUMMARY": "text-embedding-ada-002",
                                                  "GEN_TEMPLATE": "text-embedding-ada-002",
                                                  "CORE_DATA": "tbd",
                                                  "GEN_DATA": "tbd",
                                                  "CORE_CODE": "tbd",
                                                  "GEN_CODE": "tbd",
                                                  "CORE_OBJECT": "tbd",
                                                  "GEN_OBJECT": "tbd",
                                                  "CORE_IMAGE": "CLIP-ViT-B-32", 
                                                  "GEN_IMAGE": "CLIP-ViT-B-32",
                                                  "CORE_VIDEO": "tbd", 
                                                  "GEN_VIDEO": "tbd",
                                                  "CORE_AUDIO": "tbd",
                                                  "GEN_AUDIO": "tbd"}

        # list of collections and embeddings models we will use in embedDB, based on type of content
        self.content_types_and_core_collection = {"TEXT": {"core_awareness_type": "TEXT.EXTRACTED_TEXT", "core_collection": "CORE_TEXT"}, 
                                                  "DATA": {"core_awareness_type": "DATA.EXTRACTED_DATA", "core_collection": "CORE_DATA"},
                                                  "CODE": {"core_awareness_type": "CODE.EXTRACTED_CODE", "core_collection": "CORE_CODE"}, 
                                                  "JSON": {"core_awareness_type": "JSON.EXTRACTED_OBJECT", "core_collection": "CORE_OBJECT"},
                                                  "IMAGE": {"core_awareness_type": "IMAGE.EXTRACTED_BINARY", "core_collection": "CORE_IMAGE"}, 
                                                  "VIDEO": {"core_awareness_type": "VIDEO.EXTRACTED_BINARY", "core_collection": "CORE_VIDEO"}, 
                                                  "AUDIO": {"core_awareness_type": "AUDIO.EXTRACTED_BINARY", "core_collection": "CORE_AUDIO"}}


        #################################################################################################################################
        # Database Properties 

        # List of allowed sql engines
        self.allowed_engines = ["sqlite", "postgres", "mysql", "oracle", "mssql", "access", "db2", "redis", "gcloud_sql", "aws_es", "mongodb", "chromadb", "pinecone", "neo4j", "arangograph", "redisgraph", "graphdb"]

        # DB paths
        self.edrak_path = os.path.expanduser("~/tenn/edrak/") # unix & mac
        # self.edrak_path = os.path.expanduser("~\\tenn\\edrak\\") # windows

        # DB Engines
        self.standard_edrak_db_engine = "sqlite"
        self.standard_vector_db_engine = "chromadb"
        self.standard_object_db_engine = "mongodb"
        self.standard_graph_db_engine = "graphdb" # TODO figure out the graph database

        # DB Engines
        self.standard_edrak_db_hostname = "localhost"
        self.standard_vector_db_hostname = "localhost"
        self.standard_object_db_hostname = "localhost"
        self.standard_graph_db_hostname = "localhost" # TODO figure out the graph database

        # DB Engines
        self.standard_edrak_db_port = 3306
        self.standard_vector_db_port = 8000
        self.standard_object_db_port = 27017
        self.standard_graph_db_port = 0 # TODO figure out the graph database

        # DB locations
        self.standard_edrak_db_path  = self.edrak_path + "tenn_edrak.db"
        self.standard_vector_db_path = self.edrak_path + "tenn_vector.db"
        self.standard_object_db_path = self.edrak_path + "tenn_object.db"
        self.standard_graph_db_path  = self.edrak_path + "tenn_graph.db"

        # NoSQL DBs
        self.standard_no_sql_db_name    = "tenn"
        self.standard_api_db_name       = "apis"
        self.standard_object_db_name    = "objects"
        self.standard_embed_db_name     = "embeddings"
        self.standard_template_db_name  = "templates"

        #################################################################################################################################

        self.login_credentials_path = self.edrak_path + "tenn_login_credentials.yaml"

        #################################################################################################################################

        # Set the Intent properties

        self.model_map = {  # OpenAI models 
                            "text-davinci-003": {"friendly_name": "OpenAI Text Davinci 003", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-3.5-turbo": {"friendly_name": "OpenAI GPT 3.5 Turbo", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-3.5-turbo-instruct": {"friendly_name": "OpenAI GPT 3.5 Turbo Instruct", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-3.5-turbo-16k": {"friendly_name": "OpenAI GPT 3.5 Turbo 16K", "hf_model": "openai-gpt", "max_tokens": 16384},
                            "gpt-3.5-turbo-0613": {"friendly_name": "OpenAI GPT 3.5 Turbo Task", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-3.5-turbo-16k-0613": {"friendly_name": "OpenAI GPT 3.5 Turbo Task 16K", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-4": {"friendly_name": "OpenAI GPT 4", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-4-0314": {"friendly_name": "OpenAI GPT 4 0314", "hf_model": "openai-gpt", "max_tokens": 4096},
                            "gpt-4-0613": {"friendly_name": "OpenAI GPT 4 Task", "hf_model": "openai-gpt", "max_tokens": 8192},
                            
                            # Cohere models (TODO we need to fix the tokenizer model as it is not picking up a HF model)
                            # "command-nightly": {"friendly_name": "Cohere Command", "hf_model": "Cohere/command-nightly", "max_tokens": 4096},
                            "command-nightly": {"friendly_name": "Cohere Command", "hf_model": "currentlyexhausted/lite-llm-248", "max_tokens": 4096},

                            # AI21 models
                            "j2-light": {"friendly_name": "AI21 Jurassic Light", "hf_model": "currentlyexhausted/lite-llm-248", "max_tokens": 4096},
                            "j2-mid": {"friendly_name": "AI21 Jurassic Mid", "hf_model": "currentlyexhausted/lite-llm-248", "max_tokens": 4096},
                            "j2-ultra": {"friendly_name": "AI21 Jurassic Ultra", "hf_model": "currentlyexhausted/lite-llm-248", "max_tokens": 8192},

                            # Google AI models (TODO we need to figure out authentication first)
                            # "chat-bison": {"friendly_name": "Google VertexAI Chat", "hf_model": "google/chat-bison", "max_tokens": 4096},
                            # "chat-bison@001": {"friendly_name": "Google VertexAI Chat 001", "hf_model": "google/chat-bison", "max_tokens": 4096},
                            # "chat-bison-32k": {"friendly_name": "Google VertexAI Chat 32K", "hf_model": "google/chat-bison", "max_tokens": 32768},

                            # No access yet for these models
                            # "gpt-4-32k": {"friendly_name": "OpenAI GPT 4 32K", "hf_model": "openai-gpt", "max_tokens": 32768},
                            # "gpt-4-32k-0314": {"friendly_name": "OpenAI GPT 4 32K 0314", "hf_model": "openai-gpt", "max_tokens": 32768},
                            # "gpt-4-32k-0613": {"friendly_name": "OpenAI GPT 4 32K Task", "hf_model": "openai-gpt", "max_tokens": 32768},

                            # These seem old and don't work anymore
                            # "curie-001": {"friendly_name": "OpenAI Curie 001", "hf_model": "openai-gpt", "max_tokens": 2048},
                            # "babbage-001": {"friendly_name": "OpenAI Babbage 001", "hf_model": "openai-gpt", "max_tokens": 2048},
                            # "babbage-002": {"friendly_name": "OpenAI Babbage 002", "hf_model": "openai-gpt", "max_tokens": 2048},
                            # "ada-001": {"friendly_name": "OpenAI Ada 001", "hf_model": "openai-gpt", "max_tokens": 2048},
                         }

        #################################################################################################################################

        # Set the SafeAI properties
        self.safe_ai_jwt_secret = os.environ["JWT_SECRET"]
        self.safe_ai_jwt_algorithm = os.environ["JWT_ALGORITHM"]
        self.safe_ai_jwt_timeout   = os.environ["JWT_TIMEOUT"]
        self.safe_ai_standard_token_url = "tenn_token"
