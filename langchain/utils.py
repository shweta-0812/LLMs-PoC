import os

def get_api_key(key):
    """Gets the API key from an environment variable."""
    api_key = os.getenv(key)
    if not api_key:
        raise ValueError("Key environment variable is not set.")
    return api_key
