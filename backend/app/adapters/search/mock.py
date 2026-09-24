import re
from functools import lru_cache

from app.adapters.base import ServiceStatus

from .base import SearchAdapter
from .chunking import load_kb

RESULT_KEYS = ("title", "url", "agency", "lang", "topic", "content")


@lru_cache(maxsize=1)
def _chunks() -> list[dict]:
    return load_kb()


STOPWORDS = frozenset(
    [
        "a",
        "an",
        "the",
        "i",
        "me",
        "my",
        "we",
        "is",
        "are",
        "do",
        "does",
        "can",
        "what",
        "how",
        "to",
        "of",
        "for",
        "in",
        "on",
        "and",
        "or",
        "if",
        "it",
        "be",
    ]
)


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


class Adapter(SearchAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    # ponytail: word-overlap scoring, not BM25; fine for ~100 chunks
    def search(self, query: str, lang: str = "en", top: int = 5) -> list[dict]:
        terms = set(_words(query)) - STOPWORDS
        scored = []
        for chunk in _chunks():
            if chunk["lang"] != lang:
                continue
            title_words = set(_words(chunk["title"]))
            body_words = _words(chunk["content"])
            score = sum(2 * (t in title_words) + (t in body_words) for t in terms)
            matched = sum(t in title_words or t in body_words for t in terms)
            if matched >= min(2, len(terms)):  # one stray word isn't a match
                scored.append((score, {k: chunk[k] for k in RESULT_KEYS}))
        scored.sort(key=lambda s: -s[0])
        return [{**r, "score": float(s)} for s, r in scored[:top]]
