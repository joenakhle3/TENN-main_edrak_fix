import os
from PIL import Image
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils


class TENN_Image_Adapter():
    def __init__(self):
        self.utils = TENN_Utils()

    def load_and_split_data(self, passed_url):

        if not os.path.exists(passed_url):
            raise FileNotFoundError(
                f"TENN_Image_Adapter - Image not found: {passed_url}")

       # Load the image
        image = Image.open(passed_url)

        width, height = image.size

        # Convert the full image to a list of pixel values
        full_content = list(image.getdata())

        chunks_list = []

        chunk_size = (50, 50)

        for i in range(0, width, chunk_size[0]):
            for j in range(0, height, chunk_size[1]):
                left = i
                upper = j
                right = min(i + chunk_size[0], width)
                lower = min(j + chunk_size[1], height)

                # Crop the chunk from the image
                chunk = image.crop((left, upper, right, lower))

                # Convert the chunk to a list of pixel values
                chunk_pixels = list(chunk.getdata())
                chunks_list.append(chunk_pixels)
        return chunks_list, full_content