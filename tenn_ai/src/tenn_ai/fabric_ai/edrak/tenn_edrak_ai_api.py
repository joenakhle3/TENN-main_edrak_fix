
# import fastapi and base classes
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import TENN classes
from tenn_ai.fabric_ai.edrak.tenn_edrak_ai import TENN_EdrakAI
from tenn_ai.fabric_ai.edrak.databases.tenn_edrak_db import TENN_EdrakDB
# Import the utility packages
import json
from pyxtension import Json
from pydantic import BaseModel
from typing import Optional, List
from typing import Annotated
import datetime
from typing import Optional, List, Union, Dict


# API requests functions for the edrak ai

edrakDB = TENN_EdrakDB()
edrakAI = TENN_EdrakAI()
router_edrak_ai = APIRouter()
####################################################################################################
# Classes for the API requests
####################################################################################################



class TENN_Input_Request(BaseModel):
    aid: Optional[str]
    url: str
    input_type: str  # FILE, URL, API, STREAM
    hashcode: str

class TENN_Input_Contents_Request(BaseModel):
    full_content: Union[str, bytes]
    url: str
    url_type: str
    input_type: str  # FILE, URL, API, STREAM
    content_type: str  # TEXT, IMAGE, VIDEO, AUDIO, JSON, BINARY
    documents: Optional[List[Union[str, bytes]]]
    ids: Optional[List[str]]
    metadatas: Optional[List[Dict[str, str]]]


# API to invoke TENN_EdrakAI.create_or_update_core_awareness() function from TENN_EdrakAI UI
@router_edrak_ai.post("/create_or_update_core_awareness")
async def api_create_or_update_core_awareness(input_data: TENN_Input_Request, content_data: TENN_Input_Contents_Request):
    edrakAI = TENN_EdrakAI()
    edrakAI.create_or_update_core_awareness(input_data, content_data)
    return "Successfully created/updated awareness"

# API to invoke TENN_EdrakAI.delete_awareness() function from TENN_EdrakAI UI
# @router_edrak_ai.delete("/delete_awareness/{aid}")
# async def api_delete_awareness(aid: int):
#     edrakAI = TENN_EdrakAI()
#     success = edrakAI.delete_awareness(aid)
#     if success:
#         return {"status": "Successfully deleted the awareness for aid: " + aid}
#     else:
#         return {"status": "Failed to delete the awareness for aid: " + aid}

# API to invoke TENN_EdrakDB.get_all_awareness() function from TENN_EdrakDB  
@router_edrak_ai.get("/get_all_awareness")
async def api_get_all_awareness():
    return edrakDB.get_all_awareness()
