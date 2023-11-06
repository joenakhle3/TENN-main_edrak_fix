
import sys
import json
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils


class TENN_Json_Adapter():
    def __init__(self):
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_url) -> list:
        with open(passed_url) as file:
            data = json.load(file)

        full_content = json.dumps(data, indent=4)

        chunks_list = []

        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                # Process simple values as a chunk
                chunks_list.append(str(value))
            else:
                for item in value:
                    if isinstance(item, (str, int, float, bool)):
                        chunks_list.append(str(item))
                    

        return chunks_list, full_content
