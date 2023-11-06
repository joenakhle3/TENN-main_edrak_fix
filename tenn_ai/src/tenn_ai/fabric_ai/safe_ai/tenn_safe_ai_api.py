# import fastapi
from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketException, status, HTTPException
from fastapi import Cookie, Depends, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

# import TENN utilities and properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties

# import TENN safeAI classes
from tenn_ai.fabric_ai.safe_ai.tenn_safe_ai import TENN_SafeAI, TENN_JWT_Bearer
from tenn_ai.fabric_ai.safe_ai.tenn_safe_db import TENN_User, TENN_Org

# import utility packages
import json
from pyxtension import Json
from pydantic import BaseModel, Field
from typing import Set, Optional, List, Dict
from typing import Annotated


##############################################################################################################################

# Create the app
router_safe_ai = APIRouter()
properties = TENN_Properties()
utils = TENN_Utils()
safeAI = TENN_SafeAI()

# Create SafeAI controllers for security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=properties.safe_ai_standard_token_url)

##############################################################################################################################
##############################################################################################################################
# APIs
##############################################################################################################################
##############################################################################################################################

##############################################################################################################################
# API for the user to login

@router_safe_ai.post("/api/safe_ai/login")
async def api_login(token: Annotated[str, Depends(oauth2_scheme)]):

    return {"token": token}

##############################################################################################################################
# API to get the current logged in user

@router_safe_ai.get("/api/safe_ai/get_user")
async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user: TENN_User = safeAI.get_user_from_token(passed_token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        return Json(user.to_dict())

##############################################################################################################################
# API example on how to use the Depends function on the TENN_JWT_Bearer class

@router_safe_ai.post("/api/safe_ai/list_users", dependencies=[Depends(TENN_JWT_Bearer())], tags=["posts"])
def list_users(collection_name: str):
    return Json(safeAI.get_all_users())

##############################################################################################################################
# API to create a new user

@router_safe_ai.post("/api/safe_ai/signup", tags=["user"])
def create_user(user_data: Annotated[TENN_User, Depends()]):

    user = TENN_User()
    user.from_dict(user_data)

    if safeAI.create_user(user):
        return safeAI.encode_jwt(user.email)
    else:
        return {"error": "Error creating user"}

##############################################################################################################################
# API to login a user

@router_safe_ai.post("/api/safe_ai/login", tags=["user"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    email = form_data.username
    password = form_data.password

    user: TENN_User = safeAI.authenticate_user(passed_email=email, passed_password=password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        encoded_email = safeAI.encode_jwt(user.email)
        return Json({"access_token": encoded_email, "token_type": "bearer"})
    