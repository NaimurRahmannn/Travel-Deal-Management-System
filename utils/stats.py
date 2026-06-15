from collections import Counter
from threading import Lock

_lock = Lock()

_stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
}

_search_terms = Counter()   # Track search frequency


def record_request(success: bool):
    with _lock:
        _stats["total_requests"] += 1
        if success:
            _stats["successful_requests"] += 1
        else:
            _stats["failed_requests"] += 1


def record_search(destination: str):
    if destination:
        with _lock:
            _search_terms[destination.lower()] += 1


def most_searched_destination():
    with _lock:
        if not _search_terms:
            return None
        term, count = _search_terms.most_common(1)[0]
        return {"destination": term, "searches": count}


def get_stats():
    with _lock:
        return {
            "total_requests": _stats["total_requests"],
            "successful_requests": _stats["successful_requests"],
            "failed_requests": _stats["failed_requests"],
        }