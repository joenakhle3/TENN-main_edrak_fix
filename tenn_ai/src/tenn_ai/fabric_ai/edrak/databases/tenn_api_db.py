import json
import requests

from pymongo import MongoClient
from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties
from tenn_ai.fabric_ai.edrak.stores.tenn_nosql_db import TENN_NoSqlDB

from fastapi import APIRouter, HTTPException
from typing import Optional, List, Union, Dict
from pydantic import BaseModel

#########################################################################################################

# This is the structure of the JSON object that will be used to store the API data

"""
{
  "api_id": "api_unique_identifier",
  "api_name": "API Name",
  "version": "1.0.0",
  "description": "Description of the API",
  "provider": "Provider Name",
  "provider_website": "http://provider.com",
  "documentation_url": "http://api.docs.com",
  "base_url": "http://api.base.url",
  "host": "api.base.url",
  "auth_type": "OAuth2",  // could be "API Key", "Basic", "None" etc.
  "auth_details": {
    "token_url": "http://api.base.url/token",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "scope": "required_scope"
  },
  "endpoints": [
    {
      "endpoint_id": "unique_endpoint_identifier",
      "path": "/path/to/resource",
      "http_method": "GET",  // could be POST, PUT, DELETE, etc.
      "description": "Endpoint description",
      "required_parameters": [
        {
          "name": "param1",
          "type": "string",
          "location": "query"  // could be "path", "header", "body", etc.
        }
      ],
      "optional_parameters": [
        {
          "name": "optionalParam1",
          "type": "string",
          "location": "query"
        }
      ],
      "headers": [
        {
          "name": "Authorization",
          "value": "Bearer {access_token}"
        }
      ],
      "success_response_example": {
        "status_code": 200,
        "body": {
          "key": "value"
        }
      },
      "error_response_example": {
        "status_code": 404,
        "body": {
          "error": "Not Found"
        }
      }
    }
  ],
  "rate_limit": {
    "requests_per_minute": 1000,
    "concurrent_requests": 5
  }
}
"""
#########################################################################################################
#########################################################################################################
########################                    OBJECT CLASSES                         ######################
#########################################################################################################
#########################################################################################################

# This class will be used to store the API data

class TENN_Api():
    def __init__(self, passed_data=None, passed_verbose=False):
        # Convert the passed_data to a JSON string
        if passed_data is None:
            passed_data = {}
        elif isinstance(passed_data, str):
            passed_data = json.loads(passed_data)
        elif isinstance(passed_data, dict):
            pass
        
        self._api_data = passed_data
        self._verbose = passed_verbose

    def __repr__(self):
        return self._api_data.__repr__()

    # Getters and setters for all properties

    ############################################################################

    @property
    def api_data(self):
        return self._api_data

    @api_data.setter
    def api_data(self, value):
        if value is None:
            value = {}
        elif isinstance(value, str):
            value = json.loads(value)
        elif isinstance(value, dict):
            pass

        self._api_data = value

    # Getter and setter for the verbose property
    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        if not isinstance(value, bool):
            raise TypeError("verbose must be a boolean")
        self._verbose = value

    # Getters and setters for all properties
    @property
    def api_id(self):
        return self._api_data.get('api_id')

    @api_id.setter
    def api_id(self, value):
        self._api_data['api_id'] = value

    @property
    def api_name(self):
        return self._api_data.get('api_name')

    @api_name.setter
    def api_name(self, value):
        self._api_data['api_name'] = value

    @property
    def version(self):
        return self._api_data.get('version')

    @version.setter
    def version(self, value):
        self._api_data['version'] = value

    @property
    def description(self):
        return self._api_data.get('description')

    @description.setter
    def description(self, value):
        self._api_data['description'] = value

    @property
    def provider(self):
        return self._api_data.get('provider')

    @provider.setter
    def provider(self, value):
        self._api_data['provider'] = value

    @property
    def provider_website(self):
        return self._api_data.get('provider_website')

    @provider_website.setter
    def provider_website(self, value):
        self._api_data['provider_website'] = value

    @property
    def documentation_url(self):
        return self._api_data.get('documentation_url')

    @documentation_url.setter
    def documentation_url(self, value):
        self._api_data['documentation_url'] = value

    @property
    def base_url(self):
        return self._api_data.get('base_url')

    @base_url.setter
    def base_url(self, value):
        self._api_data['base_url'] = value

    @property
    def host(self):
        return self._api_data.get('host')

    @host.setter
    def host(self, value):
        self._api_data['host'] = value

    @property
    def auth_type(self):
        return self._api_data.get('auth_type')

    @auth_type.setter
    def auth_type(self, value):
        self._api_data['auth_type'] = value

    @property
    def auth_details(self):
        return self._api_data.get('auth_details')

    @auth_details.setter
    def auth_details(self, value):
        self._api_data['auth_details'] = value

    @property
    def endpoints(self):
        return self._api_data.get('endpoints')

    @endpoints.setter
    def endpoints(self, value):
        self._api_data['endpoints'] = value

    @property
    def rate_limit(self):
        return self._api_data.get('rate_limit')

    @rate_limit.setter
    def rate_limit(self, value):
        self._api_data['rate_limit'] = value
    ############################################################################
    # Serialization to JSON
    def to_json(self):
        return json.dumps(self.api_data, indent=4)

    ############################################################################
    # Deserialization from JSON
    @classmethod
    def from_json(cls, json_str):
        api_data = json.loads(json_str)
        return cls(api_data)

    ############################################################################
    # Serialization to dict
    def to_dict(self):
        return self.api_data

    ############################################################################
    # Ping an API to see if its alive
    def ping(self):
        
        try:
            # Make a GET request to the API
            response = requests.get(self.get_base_url())

            # Check if the response status code is in the success range (e.g., 200-299)
            if 200 <= response.status_code < 300:
                return True
            else:
                return False
        except Exception as e:
            if self.verbose: print("API is not accessible.")
            return False

    ############################################################################
    def invoke(self, endpoint_id, params=None) -> json:
        # Find the endpoint with the given endpoint_id
        endpoint = None
        for ep in self.endpoints:
            if ep['endpoint_id'] == endpoint_id:
                endpoint = ep
                break
                
        if endpoint is None:
            print("Endpoint not found.")
            return None

        url = f"{self.base_url}{endpoint['path']}"
        http_method = endpoint.get('http_method', 'GET')
        
        headers = {}
        for header in endpoint.get('headers', []):
            headers[header['name']] = header['value']
        
        try:
            if http_method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif http_method == 'POST':
                response = requests.post(url, json=params, headers=headers)
            else:
                if self.verbose: print(f"HTTP method {http_method} not supported in this example.")
                return None

            if response.status_code == 200:
                result_json = response.json()
                if self.verbose: print("Successful API Response:")
                if self.verbose: print(json.dumps(result_json, indent=4))
                return result_json
            else:
                if self.verbose: print(f"API Request failed with status code {response.status_code}:")
                if self.verbose: print(response.content.decode())
                return None
                
        except Exception as e:
            if self.verbose: print(f"An error occurred: {e}")
            return None


#########################################################################################################
#########################################################################################################
########################                    DATABASE CLASS                         ######################
#########################################################################################################
#########################################################################################################    
    
# This class will be used to store the API data
class TENN_ApiDB(TENN_NoSqlDB):
    
    def __init__(self, passed_db_hostname="", passed_db_port=0, passed_db_engine="", passed_verbose=False):
        self.properties = TENN_Properties()
        # Call the constructor of the parent class (TENN_NoSqlDB)
        super().__init__(passed_db_hostname, passed_db_port, passed_db_engine, passed_verbose)
        self.db_name = self.properties.standard_api_db_name
        self.collection_name = self.properties.standard_api_db_name
    
    ############################################################################
    # Override the get_collection method to use the ApiDB database and collection
    def get_collection(self):
        return super().get_or_create_collection(passed_collection_name=self.collection_name, passed_database_name=self.db_name)
    
    ############################################################################
    # Add API to the database, if it doesn't already exist
    def add_api(self, passed_api : TENN_Api):
        # Insert the API data into the database
        if passed_api is not None:
            # Check if this API already exists in the database
            api_id = passed_api.api_id
            if self.get_api(api_id) is not None:
                if self.verbose: print("API " + api_id + " already exists in the database. Skipping.")
                return None
            else:
                if self.verbose: print("Adding API to the database.")
                return super().insert_document(passed_document=passed_api.to_dict(), passed_collection_name=self.collection_name, passed_database_name=self.db_name)
        else:
          return None

    ############################################################################
    # Delete API from the database by its unique identifier
    def delete_api(self, passed_api_id):

        document_id = super().get_document_id_by_property(passed_property="api_id", passed_value=passed_api_id, passed_collection_name=self.collection_name, passed_database_name=self.db_name)
        
        # Delete the API data from the database by its ID
        return super().delete_document(passed_document_id=document_id, passed_collection_name=self.collection_name, passed_database_name=self.db_name)

    
    ############################################################################
    # Modify API data in the database
    def modify_api(self, passed_api_id, passed_new_api : TENN_Api):

        document_id = super().get_document_id_by_property(passed_property="api_id", passed_value=passed_api_id, passed_collection_name=self.collection_name, passed_database_name=self.db_name)

        # Update the API data in the database
        return super().update_document(passed_document_id=document_id, passed_new_document=passed_new_api.to_dict(), passed_collection_name=self.collection_name, passed_database_name=self.db_name)

    ############################################################################
    # Get API data from the database by its unique identifier
    def get_api(self, passed_api_id) -> TENN_Api:
        # Get the API data from the database by its ID
        document : dict = super().get_document_by_property(passed_property="api_id", passed_value=passed_api_id, passed_collection_name=self.collection_name, passed_database_name=self.db_name)

        # check if the document is not None
        if document is None:
            return None
        else:
            return TENN_Api(passed_data=document, passed_verbose=self.verbose)
    
    ############################################################################
    # Search for APIs based on its content
    def search(self, passed_search_query) -> list:
        # Construct a search_dict based on the search_query
        search_dict = {}  # Initialize an empty dictionary
        for key, value in passed_search_query.items():
            search_dict[key] = value

        # Call the search_documents_by_tuples function with the constructed search_dict
        return super().search_documents_by_tuples(passed_dict=search_dict, passed_collection_name=self.collection_name, passed_database_name=self.db_name)
    
    ############################################################################
    # Publish the API catalog which gives a list of all APIs available
    def print_catalog(self):
        # Search for all APIs in the database
        all_apis = self.search({})

        if all_apis:
            print("Available APIs Catalog:")
            for api in all_apis:
                print("API Information:")
                for key, value in api.items():
                    print(f"{key}: {value}")
                
                # Test if the API is accessible
                api_url = api.get("base_url", "No URL available")
                is_accessible = self.test_api(api_url)

                status = "Accessible" if is_accessible else "Inaccessible"
                print(f"Status: {status}\n")  # Add an empty line to separate API entries

        else:
            print("No APIs found in the catalog.")



###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################


# APIs for the TENN_ApiDB


router_api = APIRouter()
apiDB = TENN_ApiDB()

# For UI
class TENN_Api_Base(BaseModel):
    api_id: str
    api_name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    provider_website: Optional[str] = None
    documentation_url: Optional[str] = None
    base_url: Optional[str] = None
    host: Optional[str] = None
    auth_type: Optional[str] = None
    auth_details: Optional[dict] = None
    endpoints: Optional[List[dict]] = None
    rate_limit: Optional[dict] = None

class APIResponse(BaseModel):
    api_id: str
    message: str

class APIsResponse(BaseModel):
    apis: List[TENN_Api_Base]


@router_api.post("/add_api")
def add_api(api: TENN_Api_Base):
    print(api.dict())
    result = apiDB.add_api(TENN_Api(passed_data=api.dict()))
    if result:
        return {"API added successfully"}
    else:
        raise HTTPException(status_code=400, detail="API already exists or failed to add")

@router_api.get("/get_api/{api_id}", response_model=TENN_Api_Base)
def get_api(api_id: str):
    api = apiDB.get_api(api_id)
    if api:
        return api.to_dict()
    else:
        raise HTTPException(status_code=404, detail="API not found")

@router_api.post("/modify_api/{api_id}", response_model=APIResponse)
def modify_api(api_id: str, api: TENN_Api_Base):
    result = apiDB.modify_api(api_id, TENN_ApiDB(passed_data=api.dict()))
    if result:
        return {"api_id": api_id, "message": "API modified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to modify API")

@router_api.post("/delete_api/{api_id}", response_model=APIResponse)
def delete_api(api_id: str):
    result = apiDB.delete_api(api_id)
    if result:
        return {"api_id": api_id, "message": "API deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to delete API")

@router_api.get("/catalog_api")
def get_catalog():
    apis = apiDB.print_catalog()
    return {"apis": apis}