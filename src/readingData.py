# coding: utf8
import pandas as pd
import glob
import os.path

path = '../data/train'

files = [f for f in glob.glob(path + "**/*.txt", recursive=True)]
id = [os.path.splitext(os.path.basename(f))[0] for f in files]
content = []
i = 0

for f in files:
    i = i +1
    with open(f, 'r', encoding="utf8") as content_file:
        c = content_file.read()
        content.append(c)

doc_train = pd.DataFrame(
    {'id': id,
     'content': content
    })

print(doc_train)

train = pd.read_json("../data/trainQD.json")
print(train.head())
test = pd.read_json("../data/testQD.json")
print(test.head())

