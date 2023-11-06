import os
import glob
import sys

from tenn_ai.fabric_ai.input_ai.tenn_input_ai import TENN_InputAI
from tenn_ai.fabric_ai.input_ai.tenn_ingest import TENN_Ingest
# from tenn_ai.fabricAI.generate.tenn_generate_ai import TENN_GenerateAI

# ##############################################################################################################################

tenn_ingest = TENN_Ingest("~/Desktop/test/", passed_recursive=False)
tenn_ingest.create_awareness()

# TENN_Generate.start_gpt_conversation(awareness, passed_temperature = 0)
