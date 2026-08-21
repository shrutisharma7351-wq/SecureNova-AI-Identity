from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"


def retrieve_knowledge(query: str) -> str:
    """
    Simulated RAG retrieval.
    The agent provides a query and the retriever
    returns the relevant knowledge-base content.
    """

    document = DOCS_DIR / "poisoned_rag_document.txt"

    if not document.exists():
        raise FileNotFoundError(
            "Poisoned RAG document not found."
        )

    print("\n[RAG RETRIEVER]")
    print(f"Query received from agent: {query}")

    return document.read_text(encoding="utf-8")