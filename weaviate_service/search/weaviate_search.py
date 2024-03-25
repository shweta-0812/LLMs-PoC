from utils import assert_is_json
from db.weaviate_client import initialise_weaviate_client

'''
value of alpha lies in the range of [0,1]
'''


def search(schema_name, properties, query, alpha=0.5, search_type='dense', limit=1):
    wclient = initialise_weaviate_client()
    try:
        if query is None:
            return None

        db_query = wclient.query.get(schema_name, properties)

        if search_type == 'dense' and assert_is_json(str(query)):
            db_query = db_query.with_near_text(query)
        if search_type == 'sparse' and query != '':
            db_query = db_query.with_bm25(query=query)
        if search_type == 'hybrid' and query != '' and 0 <= alpha <= 1:
            db_query = db_query.with_hybrid(query=query, alpha=alpha)

        response = db_query.with_limit(limit=limit).do()
    finally:
        # Ensure the connection is closed
        wclient.close()
    return response


'''
search across text in different languages, need to set COHERE_API_KEY and COHERE_BASE_URL
'''


def multilingual_search(schema_name, properties, multilingual_query, limit=1, language='en'):
    wclient = initialise_weaviate_client()
    # multilingual_query = {"concepts": "Miejsca na wakacje w Kalifornii"}
    try:
        if multilingual_query is None or assert_is_json(str(multilingual_query)):
            return None

        db_query = (wclient.query.get(schema_name, properties)
            .with_near_text(multilingual_query)
            .with_where({
            "path": ['lang'],
            "operator": "Equal",
            "valueString": language
        }))

        response = db_query.with_limit(limit=limit).do()
    finally:
        # Ensure the connection is closed
        wclient.close()
    return response


'''RAG'''


def retrieval_augmented_generation(schema_name, properties, query, prompt, prompt_type, limit=1):
    wclient = initialise_weaviate_client()
    try:
        if query is None or assert_is_json(str(query)) or prompt is None or prompt_type is None:
            return None

        db_query = None
        if prompt_type == 'single':
            # prompt = "Write me a facebook ad about {title} using information inside {text}"
            db_query = (
                wclient.query.get(schema_name, properties)
                    .with_generate(single_prompt=prompt)
                    .with_near_text(query).with_limit(limit=limit)
            )

        if prompt_type == 'grouped_task':
            # generate_prompt = "Summarize what these posts are about in two paragraphs."
            db_query = (
                wclient.query.get(schema_name, properties)
                    .with_generate(grouped_task=prompt)  # Pass in all objects at once
                    .with_near_text(query).with_limit(limit=limit)
            )
        response = db_query.do()

    finally:
        # Ensure the connection is closed
        wclient.close()
    return response


def multilingual_retrieval_augmented_generation(schema_name, properties, multilingual_query, prompt, prompt_type, limit=1,
                                                language='en'):
    wclient = initialise_weaviate_client(cohere=True)
    try:
        if multilingual_query is None or assert_is_json(str(multilingual_query)) or prompt is None or prompt_type is None:
            return None

        db_query = None
        if prompt_type == 'single':
            # prompt = "Write me a facebook ad about {title} using information inside {text}"
            db_query = (
                wclient.query.get(schema_name, properties)
                    .with_generate(single_prompt=prompt)
                    .with_near_text(multilingual_query)
                    .with_where({
                    "path": ['lang'],
                    "operator": "Equal",
                    "valueString": language
                })

            )

        if prompt_type == 'grouped_task':
            # generate_prompt = "Summarize what these posts are about in two paragraphs."
            db_query = (
                wclient.query.get(schema_name, properties)
                    .with_generate(grouped_task=prompt)  # Pass in all objects at once
                    .with_near_text(multilingual_query)
                    .with_where({
                    "path": ['lang'],
                    "operator": "Equal",
                    "valueString": language
                })

            )

        response = db_query.with_limit(limit=limit).do()

    finally:
        # Ensure the connection is closed
        wclient.close()
    return response
