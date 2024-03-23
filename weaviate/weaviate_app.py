import requests
import json
import weaviate
from weaviate import EmbeddedOptions
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
from utils import get_api_key

WEAVIATE_API_KEY = get_api_key('WEAVIATE_API_KEY')
WEAVIATE_DB_URL = get_api_key('WEAVIATE_DB_URL')

# OPENAI_API_KEY = get_api_key('OPENAI_API_KEY')
# OPENAI_API_BASE = get_api_key('OPENAI_API_BASE')
# openai.api_key = OPENAI_API_KEY


def json_print(data):
    print(json.dumps(data, indent=2))


def sample_data_download():
    # Download the data
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    # Parse the JSON and preview it
    print(type(data), len(data))
    json_print(data[0])


'''
Create an embedded instance of Weaviate vector database
'''


def create_weaviate_client():
    client = weaviate.Client(
        url=WEAVIATE_DB_URL,
        # embedded_options=EmbeddedOptions(),
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
        # additional_headers={
        #     "X-OpenAI-BaseURL": OPENAI_API_BASE,
        #     "X-OpenAI-Api-Key": OPENAI_API_KEY
        # }
    )
    print(f"Client created? {client.is_ready()}")
    # print(json_print(client.get_meta()))
    return client.get_meta()
