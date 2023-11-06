
import pandas as pd
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#######################################################################################


class TENN_Sheet_Adapter():
    def __init__(self):
        self.splitter_params = {"chunk_size": 4000,
                                "chunk_overlap": 10, "length_function": len, }
        self.splitter_separators = ["\n\n", "\n", ".", "", "\t", "\r", " "]
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_url) -> list:
        # Convert the XLS file to CSV format
        if self.utils.get_file_extension(passed_url) in ['.xls', '.xlsx']:
            df = pd.read_excel(passed_url)
            df.to_csv("my_file.csv")
            loader = CSVLoader("my_file.csv")

        else:
            # Load the CSV file into the TENN_Sheet_Adapter
            loader = CSVLoader(passed_url)

        chunks_list = []

        content = loader.load()
        full_content = ''.join([document.page_content for document in content])

        splitter = RecursiveCharacterTextSplitter(
            separators=self.splitter_separators, keep_separator=True, **self.splitter_params)
        pages = loader.load_and_split(splitter)
        if not len(pages):
            raise ValueError("TENN_SHEET_Adapter - No data found")
        for page in pages:
            chunk = self.utils.clean_string(page.page_content)
            chunks_list.append(chunk)
            
        print(chunks_list)
        print(full_content)


        return chunks_list, full_content