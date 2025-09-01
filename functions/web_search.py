from google.genai import types
import requests
import time
import urllib.parse
from bs4 import BeautifulSoup

# --- Config ---
ALLOWED_DOMAINS = ["duckduckgo.com"]   # Only allow safe search engine domains
RATE_LIMIT_SECONDS = 5                 # Minimum seconds between searches
_last_call_time = 0                    # Track last call time

# Schema so the LLM knows how to use it
schema_web_search = types.FunctionDeclaration(
    name="web_search",
    description="Search the web for information and return top results",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query string"
            },
            "limit": {
                "type": "integer",
                "description": "Max number of results",
                "default": 3
            },
        },
        "required": ["query"],
    },
)

def web_search(query: str, limit: int = 3, **kwargs):
    """
    Safe web search wrapper:
      - Respects rate limits
      - Only allows whitelisted domains
      - Returns clean structured results
    """
    global _last_call_time
    now = time.time()

    # --- Rate limiting ---
    if now - _last_call_time < RATE_LIMIT_SECONDS:
        return {"error": f"Rate limit: wait {RATE_LIMIT_SECONDS} seconds between searches"}
    _last_call_time = now

    # --- Domain restriction ---
    domain = "duckduckgo.com"
    if domain not in ALLOWED_DOMAINS:
        return {"error": f"Domain '{domain}' not allowed"}

    try:
        encoded = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for a in soup.select(".result__a")[:limit]:
            results.append({"title": a.get_text(), "link": a["href"]})

        return results or [{"info": "No results found"}]

    except Exception as e:
        return {"error": str(e)}
