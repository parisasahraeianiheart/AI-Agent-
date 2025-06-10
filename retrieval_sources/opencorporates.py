# agents/sources/opencorporates.py
def lookup_opencorporates(name: str) -> dict:
    """
    Simulated business registration check from OpenCorporates.
    """
    return {
        "source": "opencorporates",
        "type": "business_registry",
        "target": name,
        "content": f"{name} is listed as a director in NeuroSynthetics Ltd, registered in Delaware in 2021.",
        "confidence": 0.83,
        "retrieved_at": "2025-06-08"
    }

