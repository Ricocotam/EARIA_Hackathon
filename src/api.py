from typing import List, NewType

Url = NewType("Url", str)

def send_query(query: str) -> Url:
    """Request the Qwant API."""
    raise NotImplementedError

def get_text(html_doc):
    raise NotImplementedError

def score(ground_truth: str, document: str):
    """Rouge Score."""
    raise NotImplementedError