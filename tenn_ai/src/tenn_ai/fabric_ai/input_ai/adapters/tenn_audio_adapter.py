
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
import os
import librosa


class TENN_Audio_Adapter:
    def __init__(self):
        self.utils = TENN_Utils()
        self.max_chunk_duration = 10

    def load_and_split_data(self, passed_url) -> list:

        if not os.path.exists(passed_url):
            raise FileNotFoundError(
                f"TENN_Audio_Adapter - Audio not found: {passed_url}")

        # Load the audio
        audio, sr = librosa.load(passed_url, sr=4000)
        full_content = audio

        chunks_list = []

        # Calculate the maximum chunk size based on chunk_duration
        max_chunk_size = int(self.max_chunk_duration * sr)

        # Create chunks of approximately equal length
        chunks_list = [audio[i:i + max_chunk_size]
                       for i in range(0, len(audio), max_chunk_size)]
        
    

        return chunks_list, full_content