from os import path
from tqdm import tqdm
from . import api_qwant, data

data_path = path.join(path.dirname(path.realpath(__file__)), "../data")


def eval_train(preds, docs):
    cat_doc = []
    for doc in docs:
        with open(path.join(data_path, f"train/{doc}.txt"), "r") as f:
            cat_doc.append(f.read())
    cat_doc = "\n".join(cat_doc)
    
    cat_url_doc = []
    for url in preds["items"]:
        txt = api_qwant.get_html(url["url"])
        txt = data.clean_html(txt)
        cat_url_doc.append(txt)
    print("eval", cat_url_doc)
    cat_url_doc = "\n".join(cat_url_doc)
    
    score = api_qwant.score(cat_doc, cat_url_doc)
    print(score)
    return score

def model_test(model, dataframe):
    urls = {}
    for i, (qid, question) in tqdm(dataframe.iterrows()):
        urls[qid] = get_urls(model(question))
        with open("toto.txt", "a") as f:
            f.write(str(qid) + ":" + " ".join(urls[qid]) + "\n")
    response = api_qwant.submit(urls)
    print(response)
    return float(response)
    
def get_urls(result):
    return [it["url"] for it in result["items"]]


def start_model(model, dataframe, test=True):
    evaluator = eval_train
    preds = {}
    scores = {}
    for _, (answer, docs, qid, question) in dataframe.iterrows():
        preds[qid] = model(question)
        print(preds)
        score = evaluator(preds[qid], docs)
        print(score)
        scores[qid] = score

    score = sum(scores.values()) / len(scores)
    return score