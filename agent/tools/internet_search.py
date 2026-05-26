import httpx
from os import environ


async def internet_search(
    query: str,
    max_results: int = 5,
):
    """Run a web search"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                environ["SEARXNG_URL"],
                params={"q": query, "format": "json"},
                auth=(environ["SEARXNG_USERNAME"], environ["SEARXNG_PASSWORD"]),
            )

            response.raise_for_status()
            data = response.json()

            return data.get("results", [])[:max_results]

    except httpx.TimeoutException:
        return [{"title": "搜索超时", "content": "请求超时，请稍后再试"}]
    except httpx.HTTPStatusError as e:
        return [
            {"title": "搜索失败", "content": f"HTTP 错误: {e.response.status_code}"}
        ]
    except Exception as e:
        return [{"title": "搜索异常", "content": f"错误: {str(e)}"}]
