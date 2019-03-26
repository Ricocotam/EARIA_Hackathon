import argparse
import pandas as pd

import os
from os import path

from .common import start_model, model_test
from .models import copy_paster, url_graph, kw_extraction, stopwords


parser = argparse.ArgumentParser()

parser.add_argument("model")
parser.add_argument("--test", action="store_true")

models = {"copy": copy_paster.model}

def main():
    args = parser.parse_args()
    # Load data
    # ...
    if not args.test:
        p = path.join(path.dirname(path.realpath(__file__)), "../data/trainQD.json")
        train = pd.read_json(p)
        start_model(models[args.model](), train, args.test)
    else:
        p = path.join(path.dirname(path.realpath(__file__)), "../data/testQD.json")
        test = pd.read_json(p)
        model_test(models[args.model](), test)

if __name__ == "__main__":
    main()