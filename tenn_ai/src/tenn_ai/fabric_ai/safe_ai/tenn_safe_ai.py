# import the utilities and properties
from tenn_ai.fabric_ai.utils.tenn_utils import TENN_Utils
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.utils.tenn_config_ai import TENN_ConfigAI

# import all the tenn needed classes
from tenn_ai.fabric_ai.safe_ai.tenn_safe_db import TENN_User, TENN_Org, TENN_SafeDB

# import fastapi
from fastapi import FastAPI, Request, WebSocket, WebSocketException, status, HTTPException
from fastapi import Cookie, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

# Import the utility packages
import time
import json
import jwt
from decouple import config
from pyxtension import Json
from pydantic import BaseModel, Field
from typing import Set, Optional, List, Dict
from typing import Annotated
import random
import string
import hashlib

##############################################################################################################################

# Class SafeAI is the controller for all safety and security related functions and databases

class TENN_SafeAI:
    # Define the constructor
    def __init__(self):
        self.utils = TENN_Utils()
        self.properties = TENN_Properties()
        self.safeDB = TENN_SafeDB()
        self.safeDB.connect()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.properties.safe_ai_standard_token_url)
    
    ##############################################################################################################################
    # Function to get the user by email

    def get_user(self, passed_email: str):
        return self.safeDB.get_user(passed_email=passed_email)

    ##############################################################################################################################
    # Function to get the user from the token

    def get_user_from_token(self, passed_token: str):
        decoded_token = self.decode_jwt(passed_token)
        if decoded_token:
            email = decoded_token["email"]
            if self.utils.is_valid_email(email):
                return self.get_user(decoded_token["email"])
            else: 
                return None
        else:
            return None

    ##############################################################################################################################
    # Function to check if a user exists

    def user_exists(self, passed_user: TENN_User):
        return self.safeDB.user_exists(passed_user.email)

    ##############################################################################################################################
    # Function to check if an email exists in the user database

    def email_exists(self, passed_email: str):
        return self.safeDB.user_exists(passed_email)

    ##############################################################################################################################
    # Function to check if a username exists in the user database

    def username_exists(self, passed_username: str):
        return self.safeDB.username_exists(passed_username)

    ##############################################################################################################################
    # Function to get all users from the safeDB

    def get_all_users(self):
        return self.safeDB.get_all_users()

    ##############################################################################################################################
    # Function to create a user

    def create_user(self, passed_user: TENN_User):
        if self.user_exists(passed_user):
            return None
        else:
            passed_user.email = passed_user.email.lower()
            passed_user.password = self.hash_password(passed_user.password)
            return self.safeDB.add_or_update_user(passed_user=passed_user)

    ##############################################################################################################################
    # Function to authenticate and return a user if the user exists and the password matches and the user is enabled

    def authenticate_user(self, passed_email: str, passed_password: str):
        
        # If the user does not exist, return False
        user = self.get_user(passed_email=passed_email)
        if not user:
            return None
        
        # If the user is not enabled, return False
        if not user.enabled:
            return None

        # If the passwords do not match, return False
        if not self.passwords_match(passed_password=passed_password, passed_hashed_password=user.password):
            return None
        
        return user

    ##############################################################################################################################
    # Function to verify that passwords match

    def passwords_match(self, passed_clear_password: str, passed_hashed_password: str):
        return self.hash_password(passed_clear_password) == passed_hashed_password
    
    ##############################################################################################################################
    # Function to hash a password using sha256

    def hash_password(self, passed_password: str):
        # Convert the password to bytes
        password_bytes = passed_password.encode('utf-8')
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password

    ##############################################################################################################################
    # JWT Handling
    ##############################################################################################################################

    ##############################################################################################################################
    # Define the token response function

    def token_response(self, token: str):
        return {
            self.properties.safe_ai_standard_token_url: token
        }

    ##############################################################################################################################
    # Function to encode the JWT string

    def encode_jwt(self, passed_email: str) -> Dict[str, str]:

        payload = {
            "email": passed_email,
            "expires": time.time() + self.properties.safe_ai_jwt_timeout
        }
        token = jwt.encode(payload, self.properties.safe_ai_jwt_secret, algorithm=self.properties.safe_ai_jwt_algorithm)

        return self.token_response(token)

    ##############################################################################################################################
    # Function to decode the JWT string
        
    def decode_jwt(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, self.properties.safe_ai_jwt_secret, algorithm=self.properties.safe_ai_jwt_algorithm)
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}    

    ##############################################################################################################################

    # Generate a new random N byte string

    def generate_random_string(self, N: int = 32):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(random.choice(alphabet) for i in range(N))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3
                    and any(c in string.punctuation for c in password)
                    and not any(c == '"' for c in password)):
                break
        return password


##############################################################################################################################

# Class JWT_Bearer is the holder of tokens
# The goal of this file is to check whether the reques tis authorized or not [verification of the proteced route]

class TENN_JWT_Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TENN_JWT_Bearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(TENN_JWT_Bearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="TENN_JWT_Bearer - Invalid authentication scheme.")
            
            if not self.is_valid_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="TENN_JWT_Bearer - Invalid token or expired token.")
            
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="TENN_JWT_Bearer - Invalid authorization code.")

    def is_valid_token(self, passed_token: str) -> bool:
        isTokenValid: bool = False

        try:
            safeAI = TENN_SafeAI()
            payload = safeAI.decode_jwt(passed_token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

