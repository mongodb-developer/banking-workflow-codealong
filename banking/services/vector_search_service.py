from pymongo import MongoClient
from django.conf import settings

_client = None


def _get_collection():
    global _client
    if _client is None:
        db_config = settings.DATABASES["default"]
        uri = db_config.get("HOST")
        _client = MongoClient(uri) if uri else MongoClient()
    db_name = settings.DATABASES["default"]["NAME"]
    return _client[db_name]["banking_bankingdocument"]


def semantic_search(
    query_embedding: list[float],
    limit: int = 5,
    document_type: str | None = None,
) -> list[dict]:
    """
    Run a MongoDB Atlas Vector Search against the banking documents collection.

    Returns a list of dicts with document fields plus a 'score' key.
    """
    collection = _get_collection()

    # TODO: Build the $vectorSearch aggregation pipeline
    # Stage 1 - $vectorSearch with:
    #   index: "banking_embedding_index", path: "embedding",
    #   queryVector: query_embedding, numCandidates: limit * 10, limit: limit
    #
    # Stage 2 - $project to include:
    #   _id, title, content, document_type, status, customer_name,
    #   customer_id, score: {"$meta": "vectorSearchScore"}
    #
    # If document_type is set, insert a $match stage after $vectorSearch
    pipeline = []

    results = list(collection.aggregate(pipeline))

    for doc in results:
        doc["id"] = str(doc.pop("_id"))

    return results
