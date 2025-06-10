# agents/sources/semantic_scholar.py
def search_publications(name: str) -> dict:
    """
    Simulated publication check via Semantic Scholar.
    """
    return {
        "source": "semantic_scholar",
        "type": "academic_publications",
        "target": name,
        "content": f"{name} has 12 publications related to neural-symbolic integration and cognitive architectures.",
        "confidence": 0.91,
        "retrieved_at": "2025-06-08"
    }
