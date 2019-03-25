import argparse

from models import copy_paster, url_graph, kw_extraction, stopwords


parser = argparse.ArgumentParser()

parser.add_argument("model")


def copy_paster_model():
    copy_paster.start()


models = {"copy": copy_paster_model}

def main():
    args = parser.parse_args()
    models[args.model]()

if __name__ == "__main__":
    main()