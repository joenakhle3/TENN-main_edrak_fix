from tenn_ai.fabric_ai.edrak.databases.tenn_api_db import TENN_Api
from tenn_ai.fabric_ai.edrak.databases.tenn_api_db import TENN_ApiDB
import json


# "content-type": "application/x-www-form-urlencoded",
# post_data = {
# 	"source_language": "en",
# 	"target_language": "id",
# 	"text": "What is your name?"
# }

# Example usage
api_data_example = {
    "api_id": "random_quotes_api",
    "api_name": "Random Quotes API",
    "version": "0.0.1",
    "description": "Generates a random quote",
    "provider": "Quotes 15",
    "provider_website": "",
    "documentation_url": "",
    "base_url": "https://quotes15.p.rapidapi.com",
    "host": "quotes15.p.rapidapi.com",
    "auth_type": "API Key",
    "auth_details": {
#        "token_url": "http://api.base.url/token",
#        "client_id": "your_client_id",
#        "client_secret": "your_client_secret"
#        "scope": "required_scope"
    },
    "endpoints": [
        {
            "endpoint_id": "random_quotes_api@generate_random_quote",
            "path": "/quotes/random/",
            "http_method": "GET",
            "description": "Random Quote",
            # "required_parameters": [
            #     {
            #         "name": "param1",
            #         "type": "string",
            #         "location": "query"
            #     }
            # ],
            # "optional_parameters": [
            #     {
            #         "name": "optionalParam1",
            #         "type": "string",
            #         "location": "query"
            #     }
            # ],
            "headers": [
                {
                    "name": "X-RapidAPI-Key",
                    "value": "b60d727d90msh4aeb87797395d86p1a0aecjsnd2dc9cbee971"
                },
                {
                    "name": "X-RapidAPI-Host",
                    "value": "quotes15.p.rapidapi.com"
                }
            ],
            # "success_response_example": {
            #     "status_code": 200,
            #     "body": {
            #         "key": "value"
            #     }
            # },
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
db = TENN_ApiDB(passed_verbose=True)
api = TENN_Api(passed_data = api_data_example, passed_verbose = True)
print(api)

db.add_api(api)
api : TENN_Api = db.get_api("random_quotes_api")
print(api)

# Update an attribute
api.version = '1.0.1'
db.modify_api(api.api_id, api)
api : TENN_Api = db.get_api("random_quotes_api")
print(api.version)

# Invoke one of the endpoints
result = api.invoke("random_quotes_api@generate_random_quote")

print(json.dumps(result, indent=4))
