import os
import sys
import json
import tiktoken
from tiktoken.registry import get_encoding
from transformers import AutoTokenizer

##############
import langchain
from langchain.vectorstores import chroma
from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, FlareChain, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.memory import ChatMessageHistory
from langchain_experimental.agents.agent_toolkits import create_csv_agent

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Import TENN classes
from tenn_ai.fabric_ai.utils.tenn_config_ai import TENN_ConfigAI
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
# from tenn_ai.fabric_ai.edrak.databases.tenn_embed_db import TENN_EmbedDB

# Import litellm
from litellm import litellm, completion, completion_with_retries, ModelResponse
from langchain.chat_models import ChatLiteLLM
########################################################################################################
# Define the MultiAI Response based on LiteLLM ModelResponse

class TENN_MultiAI_Response(ModelResponse):
    def __repr__(self):
        return f"ModelResponse(choices={self.choices})"

########################################################################################################
# Define the Model Response based on LiteLLM ModelResponse

class TENN_MultiAI():
    def __init__(self, passed_model: str = "text-davinci-003", passed_stream: bool = False, passed_asynchronous: bool = False, passed_verbose: bool = False):
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.stream = passed_stream
        self.asynchronous = passed_asynchronous
        self.verbose = passed_verbose
        
        self.set_model(passed_model)

    ########################################################################################################
    # Getters and setters for the model
    def get_model(self):
        return self.model
    
    def set_model(self, passed_model: str):
        self.model = self.validate_model(passed_model)
        self.model_friendly_name = self.properties.model_map[self.model]["friendly_name"]
        self.hf_model = self.properties.model_map[self.model]["hf_model"]
        self.max_tokens = self.properties.model_map[self.model]["max_tokens"]

    ########################################################################################################
    # Validate the model
    def validate_model(self, passed_model: str) -> str:
        if passed_model is None or passed_model == "":
            if self.model is None or self.model == "":
                if self.verbose: print("TENN_MultiAI - ERROR: Model is empty. Defaulting to text-davinci-003")
                return "text-davinci-003"
            else:
                return self.model
        else:
            if passed_model in self.properties.model_map.keys():
                return passed_model
            else:
                if self.verbose: print("TENN_MultiAI - ERROR: Model " + passed_model + " is not supported. Defaulting to text-davinci-003")
                return "text-davinci-003"


    ########################################################################################################
    # Calculate the number of tokens in a messages
    def count_tokens(self, passed_message: str):
        # Load the tokenizer for the specified model
        tokenizer = AutoTokenizer.from_pretrained(self.hf_model)

        # Encode the message using the tokenizer
        encoding = tokenizer.encode(passed_message)

        # Return the number of tokens in the encoding
        return len(encoding)

    ########################################################################################################
    # Calculate the remaining needed tokens to perform the OpenAI completion

    def needed_tokens(self, passed_message: str):
        # Count the number of tokens in the message
        num_prompt_tokens = self.count_tokens(passed_message)
        return self.max_tokens - num_prompt_tokens - 30

    ########################################################################################################
    # Invoke a chat completion through the selected AI model and return the response
    # TODO Add history
    # TODO Add functions
    # TODO Add assistant
    # TODO Add api_base for huggingface local
    # TODO Add local model endpoints
    # class tenn_chat:
    #     def __init__(self,vectorstore: chroma ,
    #              system_prompt: str = None,
    #              temperature: int= 0,
    #              k_value: int= 3,
    #              source : bool= True,
    #              local_model: bool= False,
    #              filter: dict= {},
    #              history:ChatMessageHistory = ChatMessageHistory() or []):
    #         self.embeddb=TENN_EmbedDB()
    #         self.properties = TENN_Properties()
    #         self.utils = TENN_Utils()
    #         self.vectorstore=vectorstore
    #         self.temperature=temperature
    #         self.k_value=k_value
    #         self.filter=filter
    #         self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    #         if history == []:
    #             self.chat_history=ChatMessageHistory()
    #         else:
    #             self.chat_history=history

    #         if local_model==False:
    #             self.llm= OpenAI(temperature = temperature)
    #         else:
                
                # self.llm = LlamaCpp(
                # model_path=self.properties_generateai.default_local_model,
                # temperature=temperature,
                # max_tokens=2000,
                # n_ctx=4000,
                # top_p=1,
                # callback_manager=self.callback_manager,
                # verbose=False

            # if system_prompt is None:
            #     self.custom_template = self.properties_generateai.standard_prompt

    def chat(self, passed_prompt: str = "", passed_history: list = [str], passed_system_prompt: str = "", passed_temperature: int = 0, passed_stream: bool = False) -> TENN_MultiAI_Response:

        # Check if the prompt is empty and return nothing
        if passed_prompt is None or passed_prompt == "":
            if self.verbose: print("TENN_MultiAI - ERROR: Prompt is empty.")
            return None
        
        # Flatten the history into a text string
        passed_history_text = ""
        for history_item in passed_history:
            passed_history_text += history_item.strip() + "\n"
        
        # The final prompt has the context history and the prompt
        full_prompt = "Context: " + passed_history_text + "Prompt: " + passed_prompt.strip()

        if self.verbose: 
            print ("-----------------------------------------------------------------------------------------")
            print ("TENN_MultiAI\n")
            print ("Model: " + self.model_friendly_name)
            print ("User prompt: " + passed_prompt)
            print ("System prompt: " + passed_system_prompt)
            print ("-----------------------------------------------------------------------------------------")
            print ("Chat history:\n" + passed_history_text)
            print ("-----------------------------------------------------------------------------------------")

        response: TENN_MultiAI_Response = completion(model = self.model,
                                                     messages = [{ "content": full_prompt, "role": "user"},
                                                                 { "content": passed_system_prompt, "role": "system"}],
                                                     max_tokens = self.needed_tokens(full_prompt + passed_system_prompt),
                                                     temperature = passed_temperature,
                                                     stream = passed_stream,
                                                    )

        # Print the response if verbose is set to True
        if self.verbose: 
            if passed_stream:
                print(self.model + " stream response: ")
                for response_chunk in response:
                    if self.verbose: print(response_chunk.choices[0].message.content + "\n")
            else:
                print(self.model + " response: " + response.choices[0].message.content + "\n")
        
        return response


    ########################################################################################################
    # Invoke a chat completion through any supported AI model and return the response

    def chat_with_model(self, passed_model: str = "", passed_prompt: str = "", passed_history: list = [], passed_system_prompt: str = "", passed_temperature: int = 0, passed_stream: bool = False) -> TENN_MultiAI_Response:

        # Set the model
        self.set_model(passed_model)
        return self.chat(passed_prompt=passed_prompt, passed_history=passed_history, passed_system_prompt=passed_system_prompt, passed_temperature=passed_temperature, passed_stream=passed_stream)


    ########################################################################################################

    # Chat with all available models

    def chat_with_models(self, passed_models: list = [], passed_prompt: str = "", passed_history: list = [], passed_system_prompt: str = "", passed_temperature: int = 0, passed_stream: bool = False) -> TENN_MultiAI_Response:
        # Check if the prompt is empty and return nothing
        if passed_models is None or len(passed_models) == 0 or passed_prompt is None or passed_prompt == "":
            if self.verbose: print("TENN_MultiAI - chat_with_models - ERROR: Models List or Prompt is empty.")
            return None

        response = TENN_MultiAI_Response()

        # Loop through all models and chat with each one
        for model in passed_models:
            self.set_model(model)
            model_response = self.chat(passed_prompt=passed_prompt, passed_history=passed_history, passed_system_prompt=passed_system_prompt, passed_temperature=passed_temperature, passed_stream=passed_stream)
            aggregated_choice = model_response.choices[0]
            print('##########################',model_response)

            # Let's aggregate the choices into one choice
            choice_contents = "[" + self.model_friendly_name + "]: "
            for choice in model_response.choices:
                choice_contents += choice.message.content.strip()
            
            aggregated_choice.message.content = choice_contents
            response.choices.append(aggregated_choice)

        return response
    
    ########################################################################################################

    # Chat with all available models
    def chat_with_all_models(self, passed_prompt: str = "", passed_history: list = [], passed_system_prompt: str = "", passed_temperature: int = 0, passed_stream: bool = False) -> TENN_MultiAI_Response:
        # Check if the prompt is empty and return nothing
        if passed_prompt is None or passed_prompt == "":
            if self.verbose: print("TENN_MultiAI - chat_all_models - ERROR: Prompt is empty.")
            return None

        models_list = []
        for key in self.properties.model_map.keys():
            models_list.append(key)
        
        return self.chat_with_models(passed_models=models_list, passed_prompt=passed_prompt, passed_history=passed_history, passed_system_prompt=passed_system_prompt, passed_temperature=passed_temperature, passed_stream=passed_stream)

    ########################################################################################################

    def chat_with_retriever(self,passed_vectore_store: chroma, passed_prompt: str = "", passed_history: list = [str], passed_system_prompt: str = "", passed_temperature: int = 0 ,passed_stream: bool = False) -> TENN_MultiAI_Response:

        # Check if the prompt is empty and return nothing
        if passed_prompt is None or passed_prompt == "":
            if self.verbose: print("TENN_MultiAI - ERROR: Prompt is empty.")
            return None
        
        # Flatten the history into a text string
        passed_history_text = ""
        for history_item in passed_history:
            passed_history_text += history_item.strip() + "\n"
        llm = ChatLiteLLM(model=self.model)
        print(self.model,"#############################################")
        question_generator = LLMChain(llm=llm, prompt=PromptTemplate.from_template(passed_system_prompt))
        doc_chain = load_qa_chain(llm, chain_type="stuff")
        qa= ConversationalRetrievalChain(
                retriever=passed_vectore_store.as_retriever(),
                question_generator=question_generator,
                combine_docs_chain=doc_chain,
                verbose=False
            )
        
        # The final prompt has the context history and the prompt
        # full_prompt = "Context: " + passed_history_text + "Prompt: " + passed_prompt.strip()



        if self.verbose: 
            print ("-----------------------------------------------------------------------------------------")
            print ("TENN_MultiAI\n")
            print ("Model: " + self.model_friendly_name)
            print ("User prompt: " + passed_prompt)
            print ("System prompt: " + passed_system_prompt)
            print ("-----------------------------------------------------------------------------------------")
            print ("Chat history:\n" + passed_history_text)
            print ("-----------------------------------------------------------------------------------------")

        response: TENN_MultiAI_Response = qa({"question": passed_prompt, "chat_history":passed_history_text })
        # Print the response if verbose is set to True
        if self.verbose: 
            if passed_stream:
                print(self.model + " stream response: ")
                for response_chunk in response:
                    if self.verbose: print(response_chunk['answer'] + "\n")
            else:
                print(self.model + " response: " + response['answer'] + "\n")
        
        return response


    ########################################################################################################
    # Invoke a chat completion through any supported AI model and return the response

    def chat_with_model_with_retriever(self, passed_model: str = "", passed_prompt: str = "", passed_history: list = [], passed_system_prompt: str = "", passed_temperature: int = 0) -> TENN_MultiAI_Response:

        # Set the model
        self.set_model(passed_model)
        return self.chat_with_retriever(passed_prompt=passed_prompt, passed_history=passed_history, passed_system_prompt=passed_system_prompt, passed_temperature=passed_temperature)


    ########################################################################################################

    # Chat with all available models

    def chat_with_models_with_retreiver(self, passed_vectore_store: chroma , passed_models: list = [], passed_prompt: str = "", passed_history: list = [], passed_system_prompt: str = "", passed_temperature: int = 0) -> TENN_MultiAI_Response:
        # Check if the prompt is empty and return nothing
        if passed_models is None or len(passed_models) == 0 or passed_prompt is None or passed_prompt == "":
            if self.verbose: print("TENN_MultiAI - chat_with_models - ERROR: Models List or Prompt is empty.")
            return None

        response = TENN_MultiAI_Response()

        # Loop through all models and chat with each one
        for model in passed_models:
            self.set_model(model)
            model_response = self.chat_with_retriever(passed_prompt=passed_prompt, passed_history=passed_history, passed_system_prompt=passed_system_prompt, passed_temperature=passed_temperature , passed_vectore_store=passed_vectore_store)
            aggregated_choice = model_response['answer']

            # Let's aggregate the choices into one choice
            choice_contents = "[" + self.model_friendly_name + "]: "
            # for choice in model_response.choices:
            #     choice_contents += choice.message.content.strip()
            
            # aggregated_choice.message.content = choice_contents
            # response.choices.append(aggregated_choice)

        return aggregated_choice