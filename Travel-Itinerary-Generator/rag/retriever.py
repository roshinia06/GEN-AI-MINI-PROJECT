from rag.vector_store import query_vector_store


def retrieve_context(destination):
    results = query_vector_store(destination)

    context = "\n".join(results[0]) if results else ""
    return context
