from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# import the basic libraries
import uvicorn
import json
from pyxtension import Json
from pydantic import BaseModel
from typing import Optional, List
from typing import Annotated
from datetime import datetime

from tenn_ai.fabric_ai.input_ai.tenn_input_ai import TENN_InputAI
from tenn_ai.fabric_ai.edrak.databases.tenn_input_db import TENN_InputDB, TENN_Input

# APIs for the TENN_InputAI
inputAI = TENN_InputAI()
inputDB = TENN_InputDB()
router_input_ai = APIRouter()


class IngestInput(BaseModel):
    urls: List[str]
    url_type: str
    force_creation: Optional[bool] = False

class InputDBInput(BaseModel):
    input_id : int
    aid : str
    url : str
    input_type : str 
    hashcode : str
    timestamp : datetime

class DeleteInputURLS(BaseModel):
    urls: List[str]

class DeleteInputURL(BaseModel):
    url: str

class DeleteInputAID(BaseModel):
    aid: str
    
# API to invoke TENN_InputAI.process_inputs() function from TENN_InputAI UI by passing a URL 
@router_input_ai.post("/process_inputs")
async def api_process_inputs(data: IngestInput):
    inputAI.process_inputs(data.urls, data.url_type, data.force_creation)
    return "Ingesting input Done"

# API to invoke TENN_InputAI.delete_inputs() function from TENN_InputAI UI by passing a URL 
@router_input_ai.post("/delete_inputs")
async def api_delete_inputs(data: DeleteInputURLS):
    inputAI.delete_inputs(data.urls)
    return "Deleting input Done"

# API to invoke TENN_InputDB.create_or_update_input() function from TENN_InputDB to add or edit in the inputDB
@router_input_ai.post("/create_or_update_input")
async def api_create_or_update_input(data: InputDBInput):
    new_input = TENN_Input(passed_aid=data.aid, passed_url=data.url, passed_input_type=data.input_type, passed_hashcode=data.hashcode)
    inputDB.create_or_update_input(new_input)
    return "Input added successfuly"

# API to invoke TENN_InputDB.delete_input() function from TENN_InputDB to delete input by aid 
@router_input_ai.post("/delete_input")
async def api_delete_input(data : DeleteInputAID):
    inputDB.delete_input(data.aid)
    return "Input deleted successfuly"

# API to invoke TENN_InputDB.delete_input_by_url() function from TENN_InputDB to delete input by single url
@router_input_ai.post("/delete_input_by_url")
async def api_delete_input_by_url(data : DeleteInputURL):
    inputDB.delete_input_by_url(data.url)
    return "Input deleted successfuly"

# API to invoke TENN_InputDB.get_all_inputs() function from TENN_InputDB  
@router_input_ai.get("/get_all_inputs")
async def api_get_all_inputs():
    return inputDB.get_all_inputs()