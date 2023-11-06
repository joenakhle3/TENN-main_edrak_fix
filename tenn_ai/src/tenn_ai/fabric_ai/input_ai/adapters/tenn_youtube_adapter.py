from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TENN_Youtube_Adapter:
    def __init__(self):
        self.splitter_params = {
            "chunk_size": 4000,
            "chunk_overlap": 10,
            "length_function": len
        }
        self.splitter_separators = [">", "/>",
                                    "\n\n", "\n", ".", "", "\t", "\r", " "]
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_url):
        loader = YoutubeLoader.from_youtube_url(
            passed_url, add_video_info=True)
        chunks_list = []
        content = loader.load()
        full_content = ''.join([document.page_content for document in content])

        splitter = RecursiveCharacterTextSplitter(
            separators=self.splitter_separators,
            keep_separator=True,
            **self.splitter_params
        )

        pages = loader.load_and_split(splitter)

        for page in pages:
            chunk = self.utils.clean_string(page.page_content)
            chunks_list.append(chunk)
      

        return chunks_list, full_content