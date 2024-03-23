import os
import json
import requests


def json_print(data):
    print(json.dumps(data, indent=2))


def sample_data_download(url):
    # Download the data
    resp = requests.get()
    data = json.loads(resp.text)  # Load data

    # Parse the JSON and preview it
    print(type(data), len(data))
    json_print(data[0])
    return data


def get_env_key(key):
    """Gets the API key from an environment variable."""
    env_key = os.getenv(key)
    if not env_key:
        raise ValueError("Key environment variable is not set.")
    return env_key
