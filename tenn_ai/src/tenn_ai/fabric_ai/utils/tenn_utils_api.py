from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils


utils = TENN_Utils()
router_utils = APIRouter()

############################################################################################################
# Classes for the TENN_Utils API
############################################################################################################

class CleanStringInput(BaseModel):
    text: str

############################################################################################################
class HashTextInput(BaseModel):
    text: str

############################################################################################################
# Routes
############################################################################################################
# API to invoke TENN_Utils.clean_string() function from TENN_Utils UI
@router_utils.post("/clean_string")
async def api_clean_string(data: CleanStringInput):
    utils = TENN_Utils()
    return {"cleaned_text": utils.clean_string(data.text)}

############################################################################################################
# API to invoke TENN_Utils.get_files_in_folder() function from TENN_Utils UI
@router_utils.get("/get_files_in_folder")
async def api_get_files_in_folder(passed_folder_path: str, passed_recursive: bool = False, passed_include_subfolder_paths: bool = False):
    utils = TENN_Utils()
    return {"files": utils.get_files_in_folder(passed_folder_path, passed_recursive, passed_include_subfolder_paths)}

############################################################################################################
# API to invoke TENN_Utils.get_relevant_file_urls() function from TENN_Utils UI
@router_utils.get("/get_relevant_file_urls")
async def api_get_relevant_file_urls(passed_url: str, passed_recursive: bool = False):
    utils = TENN_Utils()
    return {"urls": utils.get_relevant_file_urls(passed_url, passed_recursive)}

############################################################################################################
# API to invoke TENN_Utils.has_ignored_extension() function from TENN_Utils UI
@router_utils.get("/has_ignored_extension")
async def api_has_ignored_extension(passed_file_path: str):
    utils = TENN_Utils()
    return {"has_ignored_extension": utils.has_ignored_extension(passed_file_path)}

############################################################################################################
# API to invoke TENN_Utils.hash_text() function from TENN_Utils UI
@router_utils.post("/hash_text")
async def api_hash_text(data: HashTextInput):
    utils = TENN_Utils()
    return {"hash": utils.hash_text(data.text)}

############################################################################################################
# API to invoke TENN_Utils.hash_file() function from TENN_Utils UI

@router_utils.get("/hash_file")
async def api_hash_file(passed_url: str):
    utils = TENN_Utils()
    return {"hash": utils.hash_file(passed_url)}

############################################################################################################
# API to invoke TENN_Utils.get() function from TENN_Utils UI

@router_utils.get("/generate_aid")
async def api_generate_aid():
    utils = TENN_Utils()
    return {"aid": utils.generate_aid()}