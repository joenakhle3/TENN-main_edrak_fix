import os
import sys
import argparse
# Import the TENN classes
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.input_ai.adapters.tenn_multimodal_adapter import TENN_Multimodal_Adapter
from tenn_ai.fabric_ai.input_ai.tenn_input_ai import TENN_Input_Contents

##################################################################################################################################

class TENN_Ingest:
    
    def __init__(self, 
                 passed_url: str = "",
                 passed_url_type: str = "FILE",
                 passed_verbose = False
                 ):

        # Set the properties and helpers
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.url = passed_url
        self.url_type = passed_url_type
        self.verbose: bool = passed_verbose

        
    ##############################################################################################################################

    # Reads the url and returns content  

    def read_url_contents(self) -> TENN_Input_Contents:
        
        # For each url in the list of urls, create a TENN_Multimodal_Adapter for it, load the chunked embeddings and store them in the vector database
        # for url in urls:
        if self.verbose: print ("TENN_Ingest - Returning contents for url: " + self.url)

        if self.url_type == "FILE":
            # Get the multimodal adapter for the url so we can work with it
            if self.verbose: print("TENN_Ingest - read_url_contents - Reading FILE contents for :" + self.url)
            adapter = TENN_Multimodal_Adapter(passed_url = self.url, passed_url_type = self.url_type, passed_verbose = self.verbose)

            if adapter is None or adapter.url_type == "UNKNOWN":
                if self.verbose: print("TENN_Ingest - read_url_contents - URL type is unknown.")
                return None

            # Load the chunked documents and metadata from the adapter, and return the embeddings object
            return adapter.load()
        
        elif self.url_type == "URL":
            # process a URL
            if self.verbose: print("TENN_Ingest - read_url_contents - Reading URL contents for :" + self.url)
            adapter = TENN_Multimodal_Adapter(passed_url = self.url, passed_url_type = self.url_type, passed_verbose = self.verbose)

            if adapter is None or adapter.url_type == "UNKNOWN":
                if self.verbose: print("TENN_Ingest - read_url_contents - URL type is unknown.")
                return None

            # Load the chunked documents and metadata from the adapter, and return the embeddings object
            return adapter.load()
        
        elif self.url_type == "API":
            # process an API
            if self.verbose: print("TENN_Ingest - read_url_contents - Reading API contents for :" + self.url)
            return None
        
        elif self.url_type == "STREAM":
            # process a STREAM
            if self.verbose: print("TENN_Ingest - read_url_contents - Reading STREAM contents for :" + self.url)
            return None
        
        else:
            if self.verbose: print("TENN_Ingest - read_url_contents - URL type is unknown.")
            return None


    ##############################################################################################################################
