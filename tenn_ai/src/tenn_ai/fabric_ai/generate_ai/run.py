# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import argparse
import logging
import os
import sys

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.generate_ai.camel.typing import ModelType
from tenn_ai.fabric_ai.generate_ai.chatdev.chat_chain import ChatChain
from tenn_ai.fabric_ai.generate_ai.tenn_intent_ai import TENN_IntentAI

root = os.path.dirname(__file__)
sys.path.append(root)

def get_config(company):
    """
    return configuration json files for ChatChain
    user can customize only parts of configuration json files, other files will be left for default
    Args:
        company: customized configuration name under CompanyConfig/

    Returns:
        path to three configuration jsons: [config_path, config_phase_path, config_role_path]
    """
    config_dir = os.path.join(root, "CompanyConfig", company)
    print(config_dir)
    default_config_dir = os.path.join(root, "CompanyConfig", "TENN")

    config_files = [
        "ChatChainConfig.json",
        "PhaseConfig.json",
        "RoleConfig.json"
    ]

    config_paths = []

    for config_file in config_files:
        company_config_path = os.path.join(config_dir, config_file)
        default_config_path = os.path.join(default_config_dir, config_file)

        if os.path.exists(company_config_path):
            config_paths.append(company_config_path)
        else:
            config_paths.append(default_config_path)

    return tuple(config_paths)


parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--config', type=str, default="TENN",
                    help="Name of config, which is used to load configuration under CompanyConfig/")
parser.add_argument('--org', type=str, default="TENN",
                    help="Name of your organization, your task output will be stored in WareHouse/name_org_timestamp")
parser.add_argument('--task', type=str, default="Develop a social media post about the company.",
                    help="Prompt of task")
parser.add_argument('--name', type=str, default="TENN",
                    help="Name of the task, your task output will be stored in WareHouse/name_org_timestamp")
parser.add_argument('--model', type=str, default="GPT_3_5_TURBO",
                    help="GPT Model, choose from {'GPT_3_5_TURBO','GPT_4','GPT_4_32K'}")
args = parser.parse_args()


##################################################################################################################################
#     Get TENN_IntentAI Instance and run it
##################################################################################################################################

tenn_generateAI = TENN_IntentAI(passed_config = args.config, passed_org = args.org, passed_task = args.task, passed_name = args.name, passed_model = args.model, passed_verbose = True)
tenn_generateAI.run()

