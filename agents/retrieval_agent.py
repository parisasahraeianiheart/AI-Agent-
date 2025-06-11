import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

def mock_result(task, message):
    return [{
        "title": f"{task['target']}: {message}",
        "source": task['source'],
        "confidence": 0.6,
        "timestamp": time.time()
    }]

def ensure_dict_list(data, fallback_msg="No content"):
    """Ensure data is a list of dicts. Wrap strings or objects in dicts if needed."""
    if isinstance(data, list):
        wrapped = []
        for item in data:
            if isinstance(item, dict):
                wrapped.append(item)
            else:
                wrapped.append({"content": str(item), "note": fallback_msg})
        return wrapped
    elif isinstance(data, dict):
        return [data]
    else:
        return [{"content": str(data), "note": fallback_msg}]

def retrieval_agent(state: dict) -> dict:
    tasks = state.get("osint_tasks", [])
    if not tasks:
        print("⚠️ No tasks found in state for retrieval.")
        state["retrieval_results"] = []
        return state

    print(f"🔍 Beginning retrieval for {len(tasks)} tasks...")
    results = []

    for task in tasks:
        source = task.get("source", "").lower()
        target = task.get("target", "")
        task_type = task.get("task_type", "")

        query = f"{target} {task_type.replace('_', ' ')}"
        print(f"📡 Searching [{source}] for: {query}")

        try:
            if source == "linkedin":
                data = lookup_linkedin_profile(target)
                confidence = 0.9
            elif source == "twitter" or source == "twitter/x":
                data = search_twitter_mentions(target)
                confidence = 0.7
            elif source == "opencorporates" or source == "corporate registries":
                data = lookup_opencorporates(target)
                confidence = 0.75
            elif source == "google scholar" or source == "academic databases":
                data = search_publications(target)
                confidence = 0.7
            elif source in {"google", "reuters", "bloomberg", "associated press", "google news"}:
                data = search_duckduckgo(query)
                confidence = 0.6
            else:
                data = mock_result(task, "No direct integration, mocked response used.")
                confidence = 0.5

            data = ensure_dict_list(data, fallback_msg="Wrapped non-dict item")

            for item in data:
                item.update({
                    "task": task,
                    "confidence": confidence,
                    "timestamp": time.time()
                })
            results.extend(data)

        except Exception as e:
            print(f"❌ Retrieval error for task {task}: {e}")
            results.append({
                "task": task,
                "error": str(e),
                "confidence": 0.0,
                "source": source,
                "timestamp": time.time()
            })

    print(f"📥 Collected {len(results)} retrieval results.")
    state["retrieval_results"] = results
    return state

# ✅ Optional test runner
if __name__ == "__main__":
    state = {
        "osint_tasks": [
            {"task_type": "professional_profile_search", "target": "Ali Khaledi Nasab", "source": "LinkedIn"},
            {"task_type": "news_search", "target": "Ali Khaledi Nasab", "source": "Reuters"},
            {"task_type": "academic_search", "target": "Ali Khaledi Nasab", "source": "Google Scholar"},
            {"task_type": "company_registry_search", "target": "Ali Khaledi Nasab", "source": "OpenCorporates"},
            {"task_type": "social_media_lookup", "target": "Ali Khaledi Nasab", "source": "Twitter"},
            {"task_type": "financial_check", "target": "Ali Khaledi Nasab", "source": "SEC EDGAR"},
        ]
    }
    state = retrieval_agent(state)
    print("🧠 Sample Output:\n", state["retrieval_results"])