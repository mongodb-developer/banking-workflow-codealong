from voyageai.client import Client
from django.conf import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = settings.VOYAGE_API_KEY
        if not api_key:
            raise ValueError(
                "VOYAGE_API_KEY is not set. Add it to your .env file."
            )
        _client = Client(api_key=api_key)
    return _client


def generate_embedding(text: str) -> list:
    """Generate a vector embedding for the given text using Voyage AI."""
    client = _get_client()
    # TODO: Call client.embed() with [text], model="voyage-finance-2", input_type="document"
    # Return result.embeddings[0]
    pass


def generate_query_embedding(text: str) -> list:
    """Generate a query-optimised embedding for semantic search."""
    client = _get_client()
    # TODO: Call client.embed() with [text], model="voyage-finance-2", input_type="query"
    # Return result.embeddings[0]
    pass
