SCHEMAS = {
    'questions': {
        "class": "questions",
        "vectorizer": "text2vec-openai",  # Use OpenAI as the vectorizer
        "moduleConfig": {
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text",
                # "baseURL": OPENAI_API_BASE
            }
        }
    }
}