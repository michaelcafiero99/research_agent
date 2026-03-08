import os
import json
import ssl
import certifi
import urllib.request
import urllib.parse
from src.agent.logging_config import get_logger

_ssl_ctx = ssl.create_default_context(cafile=certifi.where())

logger = get_logger(__name__)


def search_twitter(query: str, max_results: int = 10) -> list:
    """
    Searches recent tweets via the Twitter API v2.
    Filters to English, non-retweet content with some minimum engagement.
    """
    token = os.getenv("TWITTER_BEARER_TOKEN", "")
    if not token:
        logger.error("TWITTER_BEARER_TOKEN is not set")
        return []

    # lang:en and -is:retweet are available on Basic tier.
    # min_faves/min_retweets require Pro tier — do not use.
    full_query = f"{query} lang:en -is:retweet"

    params = urllib.parse.urlencode({
        "query": full_query,
        "max_results": max_results,
        "sort_order": "relevancy",
        "tweet.fields": "text,public_metrics,created_at,author_id",
        "expansions": "author_id",
        "user.fields": "name,username",
    })

    req = urllib.request.Request(
        f"https://api.twitter.com/2/tweets/search/recent?{params}",
        headers={"Authorization": f"Bearer {token}"},
    )

    try:
        with urllib.request.urlopen(req, context=_ssl_ctx) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        logger.error("Twitter search failed for '%s': %s — %s", query, e, body)
        return []
    except Exception as e:
        logger.error("Twitter search failed for '%s': %s", query, e)
        return []

    tweets = data.get("data", [])
    if not tweets:
        logger.warning("No tweets found for: %s", query)
        return []

    # Build a lookup from author_id -> username
    users = {
        u["id"]: u
        for u in data.get("includes", {}).get("users", [])
    }

    results = []
    for tweet in tweets:
        metrics = tweet.get("public_metrics", {})
        author = users.get(tweet.get("author_id", ""), {})
        username = author.get("username", "unknown")
        name = author.get("name", "")

        results.append({
            "title": f"{name} (@{username}): {tweet['text'][:80]}…" if len(tweet["text"]) > 80 else f"{name} (@{username}): {tweet['text']}",
            "url": f"https://x.com/{username}/status/{tweet['id']}",
            "content": (
                f"{tweet['text']}\n"
                f"Likes: {metrics.get('like_count', 0)} | "
                f"Retweets: {metrics.get('retweet_count', 0)} | "
                f"Replies: {metrics.get('reply_count', 0)}"
            ),
        })

    return results
