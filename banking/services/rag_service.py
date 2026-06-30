from .embedding_service import generate_query_embedding
from .vector_search_service import semantic_search


def answer_query(
    question: str,
    document_type: str | None = None,
    limit: int = 5,
) -> dict:
    """
    Retrieval pipeline:
      1. Embed the question with Voyage AI
      2. Retrieve relevant documents via Atlas Vector Search
      3. Return the most relevant document context

    Returns:
        {"answer": str, "sources": list[dict]}
    """
    # Step 1: Generate a query embedding
    # Step 2: Retrieve relevant documents with semantic_search()
    # Step 3: Handle empty results — return {"answer": "No relevant documents...", "sources": []}
    # Step 4: Build context from sources (title, type, customer, status, score, content[:800])
    # Step 5: Return {"answer": context_string, "sources": sources}
    return {"answer": "Not implemented yet.", "sources": []}
