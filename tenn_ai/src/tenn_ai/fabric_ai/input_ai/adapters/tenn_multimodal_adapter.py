import os
import hashlib
import sys
import datetime

from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.input_ai.tenn_input_ai import TENN_Input_Contents

# 
from tenn_ai.fabric_ai.input_ai.adapters.tenn_pdf_adapter import TENN_PDF_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_string_adapter import TENN_String_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_text_adapter import TENN_Text_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_webpage_adapter import TENN_Webpage_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_youtube_adapter import TENN_Youtube_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_json_adapter import TENN_Json_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_word_adapter import TENN_Word_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_sheet_adapter import TENN_Sheet_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_powerpoint_adapter import TENN_Powerpoint_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_image_adapter import TENN_Image_Adapter
from tenn_ai.fabric_ai.input_ai.adapters.tenn_audio_adapter import TENN_Audio_Adapter 
# from tenn_ai.fabric_ai.input_ai.adapters.tenn_video_adapter import TENN_Video_Adapter

#######################################################################################

# The multimodal adapter class allows us to load and split data from different sources
# It can read the following url types: properties.input_types = ["FILE", "URL", "API", "STREAM"]

class TENN_Multimodal_Adapter:
    def __init__(self, passed_url: str, passed_url_type: str = "FILE", passed_verbose: bool = False):
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.verbose = passed_verbose

        self.url: str = passed_url
        self.url_type: str = passed_url_type
        self.awareness_type = "UNKNOWN" # Will be used later

        # Let's set the adapter needed
        self.adapter = None
        self.adapter_name = "UNKNOWN"
        self.content_type: str = "UNKNOWN"
        self.set_adapter_and_content_type()

        if self.verbose: print ("TENN_Multimodal_Adapter - Using Text Adapter: " + self.adapter_name)
        if self.verbose: print ("TENN_Multimodal_Adapter - Content extracted will be: " + self.content_type)
     
     
    @staticmethod
    def get_file_contents(file_path):
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if line.startswith("URL="):
                        return line.split("=", 1)[1].strip()
        except Exception as e:
            print(f"Error reading file: {e}")
        return None

    #######################################################################################
    # Get the correct adapter for the file extension
    def set_adapter_and_content_type(self) -> object:

        ###################
        # If we got a file
        if self.url_type == "FILE":

            # Let's get the extension of the file to figure out what type it is
            self.extension = self.utils.get_file_extension(self.url)

            # If we were sent a folder by mistake, return None (multimodal adapters don't process a folder)
            if os.path.isdir(self.url):
                print ("TENN_Multimodal_Adapter - get_adapter - Unsupported type FOLDER: " + self.url)
                self.adapter = None
                return

            # For text based files
            if self.extension in ['.txt']:
                self.adapter = TENN_Text_Adapter()
                self.adapter_name = "TENN_Text_Adapter"
                self.content_type = "TEXT"
                return

            # For DOC, DOCX files
            elif self.extension in ['.doc', '.docx']:
                self.adapter = TENN_Word_Adapter()
                self.adapter_name = "TENN_Word_Adapter"
                self.content_type = "TEXT"
                return

            # For PDF files
            elif self.extension == '.pdf':
                self.adapter = TENN_PDF_Adapter()
                self.adapter_name = "TENN_PDF_Adapter"
                self.content_type = "TEXT"
                return

            # For CSV, Excel files
            elif self.extension in ['.csv', '.xls', '.xlsx']:
                self.adapter = TENN_Sheet_Adapter()
                self.adapter_name = "TENN_Sheet_Adapter"
                self.content_type = "DATA"
                return

            # For PPT, PPTX files
            elif self.extension in ['.ppt', '.pptx']:
                self.adapter = TENN_Powerpoint_Adapter()
                self.adapter_name = "TENN_Powerpoint_Adapter"
                self.content_type = "TEXT"
                return

            # For JPEG, PNG, GIF, BMP files
            elif self.extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.svg']:
                self.adapter = TENN_Image_Adapter()
                self.adapter_name = "TENN_ImageTXT_Adapter"
                self.content_type = "IMAGE"
                return

            # For MP3, MP4, AVI, WAV files
            elif self.extension in ['.mp3', '.wav']:
                self.adapter = TENN_Audio_Adapter()
                self.adapter_name = "TENN_Audio_Adapter"
                self.content_type = "AUDIO"
                return

            #     # For MP4, MPEG, AVI video files
            # elif self.extension in ['.mp4', '.mpeg', '.avi']:
            #     self.adapter = TENN_Video_Adapter()
            #     self.adapter_name = "TENN_Video_Adapter"
            #     self.content_type = "VIDEO"
            #     return

            # For JSON files
            elif self.extension == '.json':
                self.adapter = TENN_Json_Adapter()
                self.adapter_name = "TENN_Json_Adapter"
                self.content_type = "OBJECT"
                return

            
            elif self.extension == '.url':
                # Read the contents of the .url file to get the listed URLs in it
                # self.url = TENN_Multimodal_Adapter.get_file_contents(self.url)
                # print(f"Extracted URL: {self.url}")  # Add this line to check the extracted URL
                self.url = self.get_file_contents(self.url) 

                if not self.url:
                    print("TENN_Multimodal_Adapter - Could not extract URL from .url file.")
                    return  # Return early since we couldn't process the .url file

                if self.url.lower().startswith("https://www.youtube.") or self.url.lower().startswith("https://youtube.") or self.url.lower().startswith("https://youtu.be/"):
                    self.content_type = "URL"
                    self.adapter = TENN_Youtube_Adapter()
                    self.adapter_name = "TENN_Youtube_Adapter"
                    self.content_type = "TEXT"
                    return

                # Check if the url is a webpage
                if self.url.lower().startswith("http"):
                    self.content_type = "URL"
                    self.adapter = TENN_Webpage_Adapter()
                    self.adapter_name = "TENN_Webpage_Adapter"
                    self.content_type = "TEXT"
                    return 

            else:
                self.content_type = "UKNOWN"
                if self.verbose: print ("TENN_Multimodal_Adapter - Unsupported URL file extension: " + self.extension)
                return

        ###################
        # If we got a URL
        elif self.url_type == "URL":

            if self.url.lower().startswith("https://www.youtube.") or self.url.lower().startswith("https://youtube.") or self.url.lower().startswith("https://youtu.be/"): 
                self.adapter = TENN_Youtube_Adapter()
                self.adapter_name = "TENN_Youtube_Adapter"
                self.content_type = "TEXT"
                return

            # Check if the url is a webpage
            if self.url.lower().startswith("http"):
                self.adapter = TENN_Webpage_Adapter()
                self.adapter_name = "TENN_Webpage_Adapter"
                self.content_type = "TEXT"
                return

        ###################
        # Unsupported type
        else:
            if self.verbose: print ("TENN_Multimodal_Adapter - Unsupported URL type: " + self.url_type)
            return
        
   

    #######################################################################################
    # Load and split the data

    def load(self) -> TENN_Input_Contents:
        if self.url_type == "UNKNOWN":
            return None

        # Structure of the TENN_Input_Contents class
        # self.verbose = passed_verbose
        # self.full_content = None # Could be a string or a binary 
        # self.url = "" # str
        # self.url_type = "" # str could be FILE, URL, API, STREAM
        # self.content_type = "" # str could be TEXT, IMAGE, VIDEO, AUDIO, JSON, BINARY
        # self.aid = None # uuid
        # self.documents = None # List of chunks, string or binary ["chunk1",         "chunk2", ...]
        # self.embeddings = None # List of lists of embeddings     [[1.1, 2.3, 3.2],  [4.5, 6.9, 4.4], ...] automatically added
        # self.ids = None # List of chunk ids                      ["id1",            "id2", ...]
        # self.metadatas = None # List of dict of tuples           [{"key": "value", "key": "value"}, {"key": "value", "key": "value"}, ...]

        contents = TENN_Input_Contents(self.verbose)
        contents.url = self.url
        contents.url_type = self.url_type
        contents.content_type = self.content_type

        # Get the full data from the multimodal adapter
        chunks_list, contents.full_content = self.adapter.load_and_split_data(self.url) ##aa1

        # Initialize the lists 
        contents.documents = []
        contents.ids = []
        contents.metadatas = [] # structure is [{"key": "value", "key": "value"},   {"key": "value", "key": "value"}, ...}]

        chunk_number = 0
        chunk_total = len(chunks_list)
        for chunk in chunks_list:
            meta_data = {}
            meta_data["url"] = self.url
            
            # Check if the url_type is URL, API, or STREAM
            if self.url_type in ["URL", "API", "STREAM"]:
                meta_data["input_timestamp"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            else:
                if self.url_type == "FILE" and os.path.isfile(self.url):
                    meta_data["input_timestamp"] = self.utils.get_file_timestamp(self.url)
                else:
                    # Handle the case where self.url is not a valid file path
                    # You might want to log an error or take appropriate action here.
                    # For example, set a default value for meta_data["input_timestamp"] or raise an exception.
                    pass

            meta_data["created_timestamp"] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:M:%S')
            meta_data["input_type"] = self.url_type
            meta_data["content_type"] = contents.content_type
            meta_data["chunk_number"] = chunk_number
            meta_data["chunk_total"] = chunk_total


            # add any other metadata here from the multimodal adapter

            # Hash the content and url to create a unique id
            # TODO rethink the IDs of chunks

            # chunk_id = hashlib.sha256((chunk + self.url).encode()).hexdigest() ##aaa1
            # Hash the content and url to create a unique id
            # Ensure that both chunk and self.url are of type str and not None
            if chunk is not None and self.url is not None:
                chunk_id = hashlib.sha256((str(chunk) + str(self.url)).encode()).hexdigest()
            else:
                # Handle the case where either chunk or self.url is None
                chunk_id = "UNKNOWN"


            contents.documents.append(chunk)
            contents.ids.append(chunk_id)
            contents.metadatas.append(meta_data) # we add the metadata from the adapter to our output

            chunk_number += 1

        return contents
    




















