from typing import List, NewType
import urllib.request as urlr
import urllib.parse as urlp
from urllib.request import Request
import re
import json

import rouge

BASEURL="http://192.168.1.1:8000/qwant"
USER="salameche"
PASSWORD="Salton123"

Url = NewType("Url", str)

def send_query(query_text: str) -> Url:
    """Request the Qwant API."""
    query="user={}&pass={}&q={}".format(urlp.quote(USER),urlp.quote(PASSWORD),urlp.quote(query_text))
    r = urlr.urlopen("{}/query?{}".format(BASEURL,query))
    response = json.loads(r.read().decode("utf-8"))
    return response

evaluator = rouge.Rouge(metrics=['rouge-n'],
                       max_n=3,
                       limit_length=True,
                       length_limit=100,
                       length_limit_type='words',
                       apply_avg='Avg',
                       apply_best='Best',
                       alpha=0.5, # Default F1_score
                       weight_factor=1.2,
                       stemming=True)

def get_html(url):
    query="user={}&pass={}&url={}".format(urlp.quote(USER),urlp.quote(PASSWORD),urlp.quote(url))
    r = urlr.urlopen("{}/document?{}".format(BASEURL,query))
    return r.read().decode("utf-8")

def score(ground_truth: str, document: str):
    """Rouge Score."""
    print(len(ground_truth), len(document))
    score = evaluator.get_scores(ground_truth, document)["rouge-3"]["f"]
    return score

def submit(run):
    query="user={}&pass={}".format(urlp.quote(USER), urlp.quote(PASSWORD))
    r = urlr.urlopen("{}/hackathon/submitrun?{}".format(BASEURL, query), data=json.dumps(run).encode("utf-8"))
    return r.read()