"""Web search through DuckDuckGo's lightweight HTML endpoint.

Only the standard library is used: the result page is fetched with
``urllib`` and result titles/links are extracted with a small
``html.parser`` subclass. Returns the top few results as plain text.
"""

from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request

_ENDPOINT = "https://html.duckduckgo.com/html/?q="
_USER_AGENT = "Mozilla/5.0 (compatible; NomiAI/1.0)"
_MAX_RESULTS = 5


def _extract_results(page: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    pattern = re.compile(
        r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL
    )
    for link, title in pattern.findall(page):
        clean_title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
        parsed = urllib.parse.urlparse(link)
        query = urllib.parse.parse_qs(parsed.query)
        real_url = urllib.parse.unquote(query.get("uddg", [link])[0])
        if "duckduckgo.com/y.js" in real_url:
            continue  # skip sponsored redirect entries
        if clean_title:
            results.append((clean_title, real_url))
        if len(results) >= _MAX_RESULTS:
            break
    return results


def run(argument: str = "") -> str:
    query = argument.strip()
    if not query:
        return "What should I search for? Try 'search latest tech news'."
    url = _ENDPOINT + urllib.parse.quote_plus(query)
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            page = response.read().decode("utf-8", errors="replace")
    except Exception:
        return "I couldn't reach the search service right now. Check your connection and try again."
    results = _extract_results(page)
    if not results:
        return f"No readable results came back for '{query}'."
    lines = [f"Top results for '{query}':"]
    for index, (title, link) in enumerate(results, start=1):
        lines.append(f"{index}. {title}\n   {link}")
    return "\n".join(lines)
