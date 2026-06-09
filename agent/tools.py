import httpx
from os import environ
from trafilatura import extract
from generate_image import generate_image_by_zit
from datetime import datetime
from pathlib import Path


async def internet_search(
    query: str,
    max_results: int = 5,
):
    """Run a web search through SearXNG"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                environ["SEARXNG_URL"],
                params={"q": query, "format": "json"},
                auth=(environ["SEARXNG_USERNAME"], environ["SEARXNG_PASSWORD"]),
                follow_redirects=True,
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


async def web_extract(
    url: str,
    include_links: bool = True,
):
    """Extract a web page"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            data = response.text
            return extract(data, output_format="markdown", include_links=include_links)
    except Exception:
        return None


async def generate_image(prompt: str, height: int = 512, width: int = 512):
    """使用Z-Image-Turbo模型进行生图"""
    try:
        img = await generate_image_by_zit(prompt, height, width)
    except Exception as e:
        return e

    save_path = str(Path.joinpath(Path.cwd(), f"{int(datetime.now().timestamp())}.png"))
    img.save(save_path)
    return "image has been saved into " + save_path
