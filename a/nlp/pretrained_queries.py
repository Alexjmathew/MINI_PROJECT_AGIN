from config import Config

def get_pretrained_response(query):
    query = query.lower().strip()
    
    # Exact matches
    if query in Config.COMMON_QUERIES:
        return Config.COMMON_QUERIES[query]
    
    # Partial matches
    for key, response in Config.COMMON_QUERIES.items():
        if key in query:
            return response
    
    return None
