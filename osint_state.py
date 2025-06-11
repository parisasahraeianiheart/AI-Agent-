from typing import TypedDict, List, Optional, Union

class OSINTState(TypedDict, total=False):
    user_query: str
    query_analysis: dict
    osint_tasks: List[dict]
    retrieval_results: List[dict]
    pivot_analysis: dict
    osint_report: str