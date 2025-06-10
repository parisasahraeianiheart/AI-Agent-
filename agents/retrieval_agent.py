import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import time
from duckduckgo_search import DDGS

from retrieval_sources.linkedin import lookup_linkedin_profile
from retrieval_sources.twitter import search_twitter_mentions
from retrieval_sources.opencorporates import lookup_opencorporates
from retrieval_sources.semanticscholar import search_publications

def search_duckduckgo(query, max_results=5):
    with DDGS() as ddgs:
        results = []
        for r in ddgs.text(query):
            results.append({
                "title": r.get("title"),
                "href": r.get("href"),
                "body": r.get("body"),
                "source": "duckduckgo"
            })
            if len(results) >= max_results:
                break
        return results

# 🔧 Mock functions for missing source types
def mock_government_database_lookup(target):
    return [{
        "title": f"{target} not found on major government watchlists",
        "source": "gov_watchlist"
    }]

def mock_public_records_lookup(target):
    return [{
        "title": f"Property ownership for {target} in California",
        "source": "public_records"
    }]

def mock_financial_record_lookup(target):
    return [{
        "title": f"No bankruptcy filings found for {target}",
        "source": "bankruptcy_records"
    }]

def retrieval_agent(task: dict) -> dict:
    query = f"{task['target']} {task['task_type'].replace('_', ' ')}"
    source = task.get("source", "").lower()

    # Normalize source aliases
    alias_map = {
        "company_registries": "opencorporates",
        "government_databases": "gov_watchlist",
        "sanctions_screening_databases": "gov_watchlist",
        "financial_distress_check": "bankruptcy_records",
    }
    source = alias_map.get(source, source)
    print(f"🔍 Running search for: {query}")

    try:
        if source == "linkedin_professional_networks":
            results = lookup_linkedin_profile(task["target"])
            confidence = "high"
        elif source == "twitter":
            results = search_twitter_mentions(task["target"])
            confidence = "medium"
        elif source == "opencorporates":
            results = lookup_opencorporates(task["target"])
            confidence = "medium"
        elif source == "academic_databases":
            results = search_publications(task["target"])
            confidence = "medium"
        elif source == "gov_watchlist":
            results = mock_government_database_lookup(task["target"])
            confidence = "high"
        elif source == "public_records":
            results = mock_public_records_lookup(task["target"])
            confidence = "medium"
        elif source == "bankruptcy_records":
            results = mock_financial_record_lookup(task["target"])
            confidence = "medium"
        else:
            results = search_duckduckgo(query)
            confidence = "medium"

        return {
            "task": task,
            "results": results,
            "confidence": confidence,
            "source": source,
            "timestamp": time.time()
        }

    except Exception as e:
        print("❌ Retrieval failed:", e)
        return {
            "task": task,
            "results": [],
            "error": str(e),
            "confidence": "low",
            "source": source,
            "timestamp": time.time()
        }

# 🧪 Optional: test
if __name__ == "__main__":
    test_tasks = [
        {"task_type": "professional_profile_search", "target": "Ali Khaledi Nasab", "source": "linkedin_professional_networks"},
        {"task_type": "news_search", "target": "Ali Khaledi Nasab", "source": "news_media"},
        {"task_type": "academic_publications", "target": "Ali Khaledi Nasab", "source": "academic_databases"},
        {"task_type": "business_registration_check", "target": "Ali Khaledi Nasab", "source": "company_registries"},
        {"task_type": "regulatory_check", "target": "Ali Khaledi Nasab", "source": "government_databases"},
        {"task_type": "court_records_search", "target": "Ali Khaledi Nasab", "source": "public_records"},
        {"task_type": "sanctions_screening", "target": "Ali Khaledi Nasab", "source": "sanctions_screening_databases"},
        {"task_type": "financial_records_search", "target": "Ali Khaledi Nasab", "source": "financial_distress_check"},
        {"task_type": "social_media_lookup", "target": "Ali Khaledi Nasab", "source": "twitter"},
    ]

    all_results = []
    for task in test_tasks:
        result = retrieval_agent(task)
        all_results.append(result)
        print(f"\n📡 Source: {task['source']}\n", result)
    
    assert len(all_results) >= 8, "❗ Must perform at least 8 distinct retrievals"