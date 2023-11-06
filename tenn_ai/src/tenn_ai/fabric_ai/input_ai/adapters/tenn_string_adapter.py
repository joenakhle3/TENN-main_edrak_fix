import sys

from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TENN_String_Adapter:
    def __init__(self):
        self.splitter_params = {"chunk_size": 5,
                                "chunk_overlap": 3, "length_function": len}
        self.splitter_separators = ["\n\n", "\n", ".", "", "\t", "\r", " "]
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_string):

        full_content = Document(page_content=passed_string)

        splitter = RecursiveCharacterTextSplitter(
            separators=self.splitter_separators, keep_separator=True, **self.splitter_params)

        chunks_list = []
        words = splitter.split_text(passed_string)

        if not len(words):
            raise ValueError("TENN_String_Adapter - No data found")

        chunks_list = []

        for word in words:
            chunk = self.utils.clean_string(word)
            chunks_list.append(chunk)

        print(full_content)
        print()
        print(chunks_list)

        return chunks_list, full_content


if __name__ == "__main__":
    test_string = input("Enter a sentence: ")
    text_adapter = TENN_String_Adapter()
    text_adapter.load_and_split_data(test_string)