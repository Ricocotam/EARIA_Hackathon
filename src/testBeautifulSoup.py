import urllib.request
from urllib.parse import urlparse
import re

def getText(page):
    # Recupération du contenu html de la page

    fp = urllib.request.urlopen(page)
    mybytes = fp.read()
    
    mystr = mybytes.decode("utf8")
    fp.close()

    # On parse le html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(mystr, 'html.parser')

    txt = [re.sub(' +',' ',(''.join(node.findAll(text=True))).replace("\t", " ").replace("\r\n",".")) for node in soup.findAll('p')]
    txt = ".".join([stri.replace("\n", "") for stri in txt])
    return(txt)

txt = getText("http://antoinegourru.com")
print(txt)
