import urllib.request
from urllib.parse import urlparse
import re

page = "http://antoinegourru.com"
# Recupération du contenu html de la page

fp = urllib.request.urlopen(page)
mybytes = fp.read()

# On récupère le nom de la source
source = urlparse(page).hostname
#print(source)

mystr = mybytes.decode("utf8")
fp.close()

# On parse le html

from bs4 import BeautifulSoup
soup = BeautifulSoup(mystr, 'html.parser')

#On récupère ici le titre de la page

#print(soup.title.string)

# On extrait les lien vers d'autre pages

x = [link.get('href') for link in soup.find_all('a')]
regex = re.compile(r'http')
selected_files = list(filter(regex.match, x))
liens = [(source,urlparse(url).hostname) for url in selected_files]
print(liens)

# On récupère tout le contenu textuel

txt = [(''.join(node.findAll(text=True))).replace("\t", " ") for node in soup.findAll('p')]
#print(txt)


