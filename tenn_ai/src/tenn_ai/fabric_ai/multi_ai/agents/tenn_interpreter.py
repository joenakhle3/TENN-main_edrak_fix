import os
import sys
import json

# Import TENN classes
from tenn_ai.src.tenn_ai.utils.tenn_config_ai import TENN_ConfigAI
from tenn_ai.src.tenn_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.src.tenn_ai.utils.tenn_utils import TENN_Utils

from interpreter import Interpreter

class TENN_Interpreter:
    def __init__(self, passed_model: str = "gpt-3.5-turbo", passed_auto_run: bool = False, passed_temperature: float = 0, passed_max_tokens: int = 100, passed_configAI: TENN_ConfigAI = None):
        self.config_ai = passed_configAI
        self.properties = TENN_Properties()
        self.utils = TENN_Utils()
        self.interpreter = Interpreter()

        self.interpreter.api_key = self.properties.openai_api_key
        self.interpreter.model = passed_model
        self.interpreter.auto_run = passed_auto_run
        self.interpreter.temperature = passed_temperature
        self.interpreter.max_tokens = passed_max_tokens

    def run(self, input_text: str):
        self.interpreter.input_text = input_text
        self.interpreter.run()
        return self.interpreter.output_text

    def set_auto_run(self, auto_run: bool):
        self.interpreter.auto_run = auto_run

    def set_model(self, model: str):
        self.interpreter.model = model

    def set_temperature(self, temperature: float):
        self.interpreter.temperature = temperature

    def set_top_p(self, top_p: float):
        self.interpreter.top_p = top_p

    def set_top_k(self, top_k: int):
        self.interpreter.top_k = top_k

    def set_max_tokens(self, max_tokens: int):
        self.interpreter.max_tokens = max_tokens
    