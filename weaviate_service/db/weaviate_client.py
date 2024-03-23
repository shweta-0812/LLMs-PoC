import requests
import json
import weaviate
# from weaviate import EmbeddedOptions # Embedded Weaviate is a new deployment model that runs a Weaviate instance from your application code rather than from a stand-alone Weaviate server installation.
from dotenv import load_dotenv, find_dotenv

from utils import get_env_key, json_print, sample_data_download
from db.weaviate_schemas import SCHEMAS

_ = load_dotenv(find_dotenv())  # read local .env file

WEAVIATE_API_KEY = get_env_key('WEAVIATE_API_KEY')
WEAVIATE_DB_HOST = get_env_key('WEAVIATE_DB_HOST')
WEAVIATE_DB_PORT = get_env_key('WEAVIATE_DB_PORT')
WEAVIATE_DB_HTTP_SECURE = get_env_key('WEAVIATE_DB_HTTP_SECURE')
WEAVIATE_DB_GRPC_HOST = get_env_key('WEAVIATE_DB_GRPC_HOST')
WEAVIATE_DB_GRPC_PORT = get_env_key('WEAVIATE_DB_GRPC_PORT')
WEAVIATE_DB_GRPC_SECURE = get_env_key('WEAVIATE_DB_GRPC_SECURE')
WEAVIATE_API_KEY = get_env_key('WEAVIATE_API_KEY')

# OPENAI_API_KEY = get_api_key('OPENAI_API_KEY')
# OPENAI_API_BASE = get_api_key('OPENAI_API_BASE')
# openai.api_key = OPENAI_API_KEY


'''
    initialise client
'''


def initialise_weaviate_client():
    return weaviate.connect_to_custom(
        http_host=WEAVIATE_DB_HOST,
        http_port=WEAVIATE_DB_PORT,
        http_secure=WEAVIATE_DB_HTTP_SECURE,
        grpc_host=WEAVIATE_DB_GRPC_HOST,
        grpc_port=WEAVIATE_DB_GRPC_PORT,
        grpc_secure=WEAVIATE_DB_GRPC_SECURE,
        auth_credentials=weaviate.auth.AuthApiKey(WEAVIATE_API_KEY)
        # headers={
        #     "X-OpenAI-Api-Key": OPENAI_API_KEY  # Or any other inference API keys,
        #     "X-OpenAI-BaseURL": OPENAI_API_BASE,
        # }
    )


'''
Create an embedded instance of Weaviate vector database
'''


def create_weaviate_client():
    wclient = initialise_weaviate_client()
    try:
        print(f"Client created? {wclient.is_ready()}")
        meta_data = wclient.get_meta()
    finally:
        # Ensure the connection is closed
        wclient.close()
    return meta_data


def create_db_collection(schema_name):
    wclient = initialise_weaviate_client()
    try:
        if not wclient.schema.exists(schema_name):
            schema_class_obj = SCHEMAS[schema_name]
            wclient.schema.create_class(schema_class_obj)
    finally:
        # Ensure the connection is closed
        wclient.close()
    return True


def reset_db_collection(schema_name):
    wclient = initialise_weaviate_client()
    try:
        # resetting the schema
        # CAUTION: This will delete your collection
        if wclient.schema.exists(schema_name):
            wclient.schema.delete_class(schema_name)
        schema_class_obj = SCHEMAS[schema_name]
        wclient.schema.create_class(schema_class_obj)
    finally:
        # Ensure the connection is closed
        wclient.close()
    return True


def load_sample_data(schema_name, batch_size=5):
    data = sample_data_download(
        url='https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')

    wclient = initialise_weaviate_client()
    try:
        with wclient.batch.configure(batch_size=batch_size) as batch:
            for i, d in enumerate(data):  # Batch import data
                properties = {
                    "answer": d["Answer"],
                    "question": d["Question"],
                    "category": d["Category"],
                }

                batch.add_data_object(
                    data_object=properties,
                    class_name=schema_name
                )

        # verify data count
        count = wclient.query.aggregate(schema_name).with_meta_count().do()
    finally:
        # Ensure the connection is closed
        wclient.close()
    return count
