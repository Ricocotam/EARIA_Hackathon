import argparse

from .common import start_model
from .models import copy_paster, url_graph, kw_extraction, stopwords


parser = argparse.ArgumentParser()

parser.add_argument("model")
parser.add_argument("--train", action="store_true")

models = {"copy": copy_paster.model}

def main():
    args = parser.parse_args()
    # Load data
    # ...
    train, test = None, None
    if args.train:
        start_model(models[args.model](), train)
    else:
        start_model(models[args.model](), test)

if __name__ == "__main__":
    main()