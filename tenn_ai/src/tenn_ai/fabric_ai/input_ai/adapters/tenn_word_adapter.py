from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TENN_Word_Adapter:

    def __init__(self):
        self.splitter_params = {"chunk_size": 4000,
                                "chunk_overlap": 10, "length_function": len, }
        self.splitter_separators = ["\n\n", "\n", ".", "", "\t", "\r", " "]
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_url) -> list:
        loader = Docx2txtLoader(passed_url)
        content = loader.load()
        full_content = ''.join([document.page_content for document in content])
        chunks_list = []

        splitter = RecursiveCharacterTextSplitter(
            separators=self.splitter_separators, keep_separator=True, **self.splitter_params)
        pages = loader.load_and_split(splitter)
        if not len(pages):
            raise ValueError("TENN_Word_Adapter - No data found")
        for page in pages:
            chunk = self.utils.clean_string(page.page_content)
            chunks_list.append(chunk)
            
        return chunks_list, full_content