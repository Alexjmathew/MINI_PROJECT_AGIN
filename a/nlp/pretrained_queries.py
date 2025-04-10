from config import Config

def get_pretrained_response(query):
    query = query.lower().strip()
    
    # Fix: Use PRETRAINED_QUERIES instead of COMMON_QUERIES
    # Exact matches
    if query in Config.PRETRAINED_QUERIES:
        return Config.PRETRAINED_QUERIES[query]
    
    # Partial matches
    for key, response in Config.PRETRAINED_QUERIES.items():
        if key in query:
            return response
    
    return None
