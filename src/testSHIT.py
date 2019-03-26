# coding: utf8
import pandas as pd
import glob
import os.path
from urllib.parse import urlparse

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

import re
def extractURLs(fileContent):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fileContent.lower())
    cleanUrls = []
    for url in urls:
        lastChar = url[-1] # get the last character
        # if the last character is not (^ - not) an alphabet, or a number,
        # or a '/' (some websites may have that. you can add your own ones), then enter IF condition
        if (bool(re.match(r'[^a-zA-Z0-9/]', lastChar))): 
            cleanUrls.append(url[:-1]) # stripping last character, no matter what
        else:
            cleanUrls.append(url) # else, simply append to new list

    return cleanUrls

URLs = [extractURLs(file) for file in content]
print("done")
import itertools
merged = list(itertools.chain(*URLs))
print(merged[0])

out = []
for url in merged:
    try:
        out.append(urlparse(url).hostname)
    except:
        True

sites = set(out)

from collections import Counter
bob = Counter(out)

bob = list(bob.items())

somme = sum([i[1]for i in bob])

# Ici on a les différents sites
voca = [i[0] for i in bob]
#la on a le tf
tf = [i[1]/somme for i in bob]


