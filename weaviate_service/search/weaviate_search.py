
def dense_search(wclient):
    response = (
        wclient.query
            .get("questions", ["question", "answer"])
            .with_near_text({"concepts": ["animal"]})
            .with_limit(3)
            .do()
    )

    return response

def sparse_search(wclient):
    response = (
        wclient.query
            .get("questions", ["question", "answer"])
            .with_bm25(query="animal")
            .with_limit(3)
            .do()
    )

    return response

'''
value of alpha lies in the range of [0,1]
'''
def hybrid_search(wclient, alpha=0.5):
    response = (
        wclient.query
            .get("questions", ["question", "answer"])
            .with_hybrid(query="animal", alpha=alpha)
            .with_limit(3)
            .do()
    )
    return response
