import requests


def internet_search(
    query: str,
    max_results: int = 5,
):
    """Run a web search"""
    data = requests.get(
        "http://localhost:8080",
        params={"q": query, "max_results": max_results, "format": "json"},
    ).json()
    return data.get("results", [])[:max_results]
