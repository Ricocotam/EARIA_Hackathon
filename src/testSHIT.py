# coding: utf8
import pandas as pd
import glob
import os.path
from urllib.parse import urlparse
from urllib.request import urlopen
from typing import List, NewType
import urllib.request as urlr
import urllib.parse as urlp
from urllib.request import Request
import re
import json


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
import itertools
merged = list(itertools.chain(*URLs))

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

def getText(page):
    # Recupération du contenu html de la page
    fp = urlopen(page)
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()

    # On parse le html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(mystr, 'html.parser')

    txt = [re.sub(' +',' ',(''.join(node.findAll(text=True))).replace("\t", " ").replace("\r\n",".")) for node in soup.findAll('p')]
    txt = ".".join([stri.replace("\n", "") for stri in txt])
    return(txt)

run = {}
compteur = 1
with open("../data/toto.txt", "r") as f:
    for line in f:
        print(compteur)
        out = line.split(":")
        qid = out.pop(0)
        urls = ":".join(out)
        urls = urls.split(" ")
        names = [urlparse(url).hostname for url in urls]
        freq = []
        for n in names:
            try:
                freq.append(tf[voca.index(n)])
            except:
                freq.append(0)
        urls = [x for _,x in sorted(zip(freq,urls))]
        out = ""
        for i in range(15):
            try:
                stout = getText(urls[i])
                out = "\n".join([out,stout])
                print("mop")
                run[qid] = out
            except:
                True
    
        compteur = compteur + 1

import json
with open("bob.json", "wb") as f:
    f.write(json.dumps(run).encode("utf-8"))
