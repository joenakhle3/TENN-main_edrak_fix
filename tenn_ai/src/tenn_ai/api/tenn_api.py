# from flask import Flask, request, jsonify

# import the utilities and properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties

# import the tenn.ai routers
from tenn_ai.fabric_ai.utils.tenn_utils_api import router_utils
from tenn_ai.fabric_ai.organize_ai.tenn_organize_ai_api import router_organize_ai
from tenn_ai.fabric_ai.input_ai.tenn_input_ai_api import router_input_ai
from tenn_ai.fabric_ai.edrak.tenn_edrak_ai_api import router_edrak_ai
# from tenn_ai.fabric_ai.safe_ai.tenn_safe_ai_api import router_safe_ai

# import the tenn.ai classes
from tenn_ai.fabric_ai.multi_ai.tenn_multi_ai import TENN_MultiAI, TENN_MultiAI_Response
# from tenn_ai.fabric_ai.safe_ai.tenn_safe_db import User, create_db_and_tables, UserCreate, UserRead, UserUpdate
# from tenn_ai.fabric_ai.safe_ai.tenn_user_manager import auth_backend, current_active_user, fastapi_users

# import the fastapi libraries
from fastapi import FastAPI, Request, WebSocket, WebSocketException, status, HTTPException
from fastapi import Cookie, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# import the basic libraries
import uvicorn
import json
from pyxtension import Json
from pydantic import BaseModel
from typing import Optional, List
from typing import Annotated

##############################################################################################################################

# Create the app
app = FastAPI()

# APIs for the TENN_OrganizeAI
app.include_router(router_organize_ai, prefix="/api/organize_ai", tags=["OrganizeAI"])  

# APIs for the TENN_EdrakAI
app.include_router(router_edrak_ai, prefix="/api/edrak_ai", tags=["EdrakAI"])

# APIs for the TENN_InputAI
app.include_router(router_input_ai, prefix="/api/input_ai", tags=["InputAI"])

# APIs for the utilities
app.include_router(router_utils, prefix="/api/utils", tags=["Utils"])

# APIs for safeAI
# app.include_router(router_safe_ai, prefix="/api/safe_ai", tags=["SafeAI"])

# Provides /login and /logout routes for a given authentication backend.
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend), 
#     prefix="/api/safe_ai", 
#     tags=["auth"]
# )

# # Provides /register routes to allow a user to create a new account.
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/api/safe_ai",
#     tags=["auth"],
# )

# # Provides /forgot-password and /reset-password routes to allow a user to reset its password.
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/api/safe_ai",
#     tags=["auth"],
# )

# # Provides /request-verify-token and /verify routes to manage user e-mail verification.
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/api/safe_ai",
#     tags=["auth"],
# )

# # Provides /me as a current authenticated active user. Also provides GET /{user_id} and PATCH /{user_id} and DELETE /{user_id} routes to manage users.
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False),
#     prefix="/api/safe_ai/users",
#     tags=["users"],
# )

##############################################################################################################################
utils = TENN_Utils()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##############################################################################################################################
# Function to get the cookie or token from the websocket

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

##############################################################################################################################
# Class to manage the websocket connections centrally 

class TENN_ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message_text(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_message_json(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_text(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = TENN_ConnectionManager()


##############################################################################################################################
##############################################################################################################################
# APIs
##############################################################################################################################
##############################################################################################################################

##############################################################################################################################
# Health check API

@app.get("/")
@app.get("/api")
async def api_health_check():
    return {"TENN.ai Server Status": "OK"}

##############################################################################################################################
# API to invoke the chat function in generateAI

# Expected JSON format:
# {
#     "history": "This is the history",
#     "prompt": "This is the prompt",
#     "system": "This is the system"
#     "model": "This is the model",
#     "temperature": 0

# TODO Convert this to use generateAI using a standard JSON object TENN_ConfigAI

@app.post("/api/chat")
async def api_post_chat(request: Request):
    data: Json(request.json())
    history = data.history
    prompt = data.prompt
    system = data.system
    model = data.model
    temperature = data.temperature
    
    # Generate a response using the chatbot
    chatbot = TENN_MultiAI()
    chatbot.set_model(model)
    response = chatbot.chat(passed_prompt=prompt, passed_system_prompt=system, passed_temperature=temperature)

    # Return the response as a JSON object
    return json.dumps(response.to_dict_recursive(), indent=4)

##############################################################################################################################
# API to invoke the chat function in generateAI

@app.get("/api/get_chat/{prompt}")
async def api_get_chat_answer(prompt: str):
    
    # Generate a response using the chatbot
    chatbot = TENN_MultiAI(passed_model="text-davinci-003", passed_verbose=True)
    response: TENN_MultiAI_Response = chatbot.chat(passed_prompt=prompt, passed_temperature=0.3)

    return json.dumps(response.to_dict_recursive(), indent=4)

##############################################################################################################################
# API to display the chat page

with open("chat.html", "r") as file:
    chat_page = file.read()

@app.get("/api/chat")
async def get():
    return HTMLResponse(chat_page)

##############################################################################################################################
# API to get a list of all the models from our properties file

@app.get("/api/get_all_models")
async def api_get_all_models():
    properties = TENN_Properties()
    return properties.model_map.keys()

##############################################################################################################################
##############################################################################################################################
# WebSockets
##############################################################################################################################
##############################################################################################################################

##############################################################################################################################  
# WebSocket for the chat function in generateAI
model = "gpt-3.5-turbo"
chatbot = TENN_MultiAI(passed_model=model, passed_verbose=True)
history = []
system = "You are a helpful AI assistant called TENN. You are concise, professional, polite, and you answer with short and accurate sentences. Do not repeat your name or the user name before your answer, and do not say any profanity or bad words."

@app.websocket("/ws/chat/{client_id}")
async def chat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            post = await websocket.receive_json()
            prompt = post["prompt"].strip()
        
            response_json = json.dumps({"response": "User(" + client_id + "): " +  utils.string_to_html(prompt)})
            await manager.broadcast_text(response_json)

            # Generate a response using the chatbot
            response: TENN_MultiAI_Response = chatbot.chat(passed_prompt=prompt, passed_history=history, passed_system_prompt=system, passed_temperature=0)
            # full_response = json.dumps(response.to_dict_recursive(), indent=4)
            answer = response.choices[0].message.content.strip()
            history.append("User(" + client_id + "): " + prompt)
            history.append("TENN: " + answer)

            response_json = json.dumps({"response": "TENN(" + model + "): " + utils.string_to_html(answer)})
            # print(response_json)
            await manager.broadcast_text(response_json)
            # await websocket.send_text(response_json)
    except WebSocketException:
        manager.disconnect(websocket)
        response_json = json.dumps({"response": "User(" + client_id + ") left the chat"})
        await manager.broadcast_text(response_json)
        await websocket.close()

##############################################################################################################################
##############################################################################################################################
# Server Main 
##############################################################################################################################
##############################################################################################################################



##############################################################################################################################

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)

