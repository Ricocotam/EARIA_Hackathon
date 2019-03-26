import rouge
import nltk
import os
import re #import the regular expressions library; will be used to strip punctuation
import pandas
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from collections import Counter #allows for counting the number of occurences in a list
from nltk.corpus import wordnet
from sklearn.model_selection import train_test_split
import urllib.request
from urllib.parse import urlparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

def getText(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    source = urlparse(url).hostname

    mystr = mybytes.decode("utf8")
    fp.close()

    # On parse le html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(mystr, 'html.parser')

    
    txt = [re.sub(' +',' ',(''.join(node.findAll(text=True))).replace("\t", " ").replace("\r\n",".")) for node in soup.findAll('p')]
    txt = " ".join([stri.replace("\n", "") for stri in txt])
    return(txt)

# getting the nltk tokens from a text
def get_tokens(raw, encoding = 'utf8'):
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(raw.lower())
	return tokens


# creating an nltk text using the passed argument (raw) after filtering out the commas
def get_nltk_text(raw, encoding = 'utf8'):
	#filter out all the commas, periods, and appostrophes using regex
	no_commas = re.sub(r'[.|,|\']',' ', raw)
	tokens = nltk.word_tokenize(no_commas)
	text = nltk.Text(tokens, encoding) # create a nltk text from those tokens
	return text

# returns the veronis stopwords in unicode, or if any other value is passed, it returns the default nltk french stopwords
def get_stopwords(type = 'veronis'):
	if type == 'veronis':
		raw_stopword_list = ["Ap.", "Apr.", "GHz", "MHz", "USD", "a", "afin", "ah", "ai", "aie", "aient", "aies", "ait", "alors", "après", "as", "attendu", "au", "au-delà", "au-devant", "aucun", "aucune", "audit", "auprès", "auquel", "aura", "aurai", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autour", "autre", "autres", "autrui", "aux", "auxdites", "auxdits", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", "avions", "avons", "ayant", "ayez", "ayons", "b", "bah", "banco", "ben", "bien", "bé", "c", "c'", "c'est", "c'était", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "celà", "cent", "cents", "cependant", "certain", "certaine", "certaines", "certains", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "cf.", "cg", "cgr", "chacun", "chacune", "chaque", "chez", "ci", "cinq", "cinquante", "cinquante-cinq", "cinquante-deux", "cinquante-et-un", "cinquante-huit", "cinquante-neuf", "cinquante-quatre", "cinquante-sept", "cinquante-six", "cinquante-trois", "cl", "cm", "cm²", "comme", "contre", "d", "d'", "d'après", "d'un", "d'une", "dans", "de", "depuis", "derrière", "des", "desdites", "desdits", "desquelles", "desquels", "deux", "devant", "devers", "dg", "différentes", "différents", "divers", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dl", "dm", "donc", "dont", "douze", "du", "dudit", "duquel", "durant", "dès", "déjà", "e", "eh", "elle", "elles", "en", "en-dehors", "encore", "enfin", "entre", "envers", "es", "est", "et", "eu", "eue", "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "eûmes", "eût", "eûtes", "f", "fait", "fi", "flac", "fors", "furent", "fus", "fusse", "fussent", "fusses", "fussiez", "fussions", "fut", "fûmes", "fût", "fûtes", "g", "gr", "h", "ha", "han", "hein", "hem", "heu", "hg", "hl", "hm", "hm³", "holà", "hop", "hormis", "hors", "huit", "hum", "hé", "i", "ici", "il", "ils", "j", "j'", "j'ai", "j'avais", "j'étais", "jamais", "je", "jusqu'", "jusqu'au", "jusqu'aux", "jusqu'à", "jusque", "k", "kg", "km", "km²", "l", "l'", "l'autre", "l'on", "l'un", "l'une", "la", "laquelle", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "lez", "lors", "lorsqu'", "lorsque", "lui", "lès", "m", "m'", "ma", "maint", "mainte", "maintes", "maints", "mais", "malgré", "me", "mes", "mg", "mgr", "mil", "mille", "milliards", "millions", "ml", "mm", "mm²", "moi", "moins", "mon", "moyennant", "mt", "m²", "m³", "même", "mêmes", "n", "n'avait", "n'y", "ne", "neuf", "ni", "non", "nonante", "nonobstant", "nos", "notre", "nous", "nul", "nulle", "nº", "néanmoins", "o", "octante", "oh", "on", "ont", "onze", "or", "ou", "outre", "où", "p", "par", "par-delà", "parbleu", "parce", "parmi", "pas", "passé", "pendant", "personne", "peu", "plus", "plus_d'un", "plus_d'une", "plusieurs", "pour", "pourquoi", "pourtant", "pourvu", "près", "puisqu'", "puisque", "q", "qu", "qu'", "qu'elle", "qu'elles", "qu'il", "qu'ils", "qu'on", "quand", "quant", "quarante", "quarante-cinq", "quarante-deux", "quarante-et-un", "quarante-huit", "quarante-neuf", "quarante-quatre", "quarante-sept", "quarante-six", "quarante-trois", "quatorze", "quatre", "quatre-vingt", "quatre-vingt-cinq", "quatre-vingt-deux", "quatre-vingt-dix", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf", "quatre-vingt-dix-sept", "quatre-vingt-douze", "quatre-vingt-huit", "quatre-vingt-neuf", "quatre-vingt-onze", "quatre-vingt-quatorze", "quatre-vingt-quatre", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-sept", "quatre-vingt-six", "quatre-vingt-treize", "quatre-vingt-trois", "quatre-vingt-un", "quatre-vingt-une", "quatre-vingts", "que", "quel", "quelle", "quelles", "quelqu'", "quelqu'un", "quelqu'une", "quelque", "quelques", "quelques-unes", "quelques-uns", "quels", "qui", "quiconque", "quinze", "quoi", "quoiqu'", "quoique", "r", "revoici", "revoilà", "rien", "s", "s'", "sa", "sans", "sauf", "se", "seize", "selon", "sept", "septante", "sera", "serai", "seraient", "serais", "serait", "seras", "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sinon", "six", "soi", "soient", "sois", "soit", "soixante", "soixante-cinq", "soixante-deux", "soixante-dix", "soixante-dix-huit", "soixante-dix-neuf", "soixante-dix-sept", "soixante-douze", "soixante-et-onze", "soixante-et-un", "soixante-et-une", "soixante-huit", "soixante-neuf", "soixante-quatorze", "soixante-quatre", "soixante-quinze", "soixante-seize", "soixante-sept", "soixante-six", "soixante-treize", "soixante-trois", "sommes", "son", "sont", "sous", "soyez", "soyons", "suis", "suite", "sur", "sus", "t", "t'", "ta", "tacatac", "tandis", "te", "tel", "telle", "telles", "tels", "tes", "toi", "ton", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "trente-cinq", "trente-deux", "trente-et-un", "trente-huit", "trente-neuf", "trente-quatre", "trente-sept", "trente-six", "trente-trois", "trois", "très", "tu", "u", "un", "une", "unes", "uns", "v", "vers", "via", "vingt", "vingt-cinq", "vingt-deux", "vingt-huit", "vingt-neuf", "vingt-quatre", "vingt-sept", "vingt-six", "vingt-trois", "vis-à-vis", "voici", "voilà", "vos", "votre", "vous", "w", "x", "y", "z", "zéro", "à", "ç'", "ça", "ès", "étaient", "étais", "était", "étant", "étiez", "étions", "été", "étée", "étées", "étés", "êtes", "être", "ô"]
	else:
		raw_stopword_list = stopwords.words('french')
	stopword_list = raw_stopword_list
	return stopword_list

# normalizes the words by turning them all lowercase and then filters out the stopwords
def filter_stopwords(text, stopword_list):
	 words = [w.lower() for w in text]
	 # filtering stopwords
	 filtered_words = []
	 for word in words:
	 	if word not in stopword_list and word.isalpha() and len(word) > 1:
	 		filtered_words.append(word)
	 return filtered_words

# stems the word list using the French Stemmer
def stem_words(words):
	stemmed_words = []
	stemmer = FrenchStemmer()
	for word in words:
		stemmed_word = stemmer.stem(word)
		stemmed_words.append(stemmed_word)
	return stemmed_words


# returns a sorted dictionary (as tuples) based on the value of each key
def sort_dictionary(dictionary):
	return sorted(dictionary.items(), key = lambda x: x[1], reverse = True)


def normalize_counts(counts):
	total = sum(counts.values())
	return dict((word, float(count)/total) for word,count in counts.items())

# print the results of sort_dictionary
def print_sorted_dictionary(tuple_dict):
    for tup in tuple_dict:
        print (unicode(tup[1])[0:10] + '\t\t' + unicode(tup[0]))


def print_words(words):
	for word in words:
		print (word)


def preprocess(description):
        description = description.lower()
        french_stopwords = get_stopwords()
        tokens = get_tokens(description)
        wordsNonstop = filter_stopwords(tokens, french_stopwords)
        return wordsNonstop

#Extension de la requette

def expand_query(query):
    from itertools import chain
    query = get_tokens(query)
    expanded_query = [getSynonyms(word) for word in query]
    unlisted_query = list(set(chain(*expanded_query)))
    return(unlisted_query )


def getSynonyms(word):
    synonyms = []
    synonyms.append(word)
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return(synonyms)        


query = "loi auteur"

txt = getText("https://www.lemonde.fr/pixels/article/2019/03/26/la-controversee-directive-sur-le-droit-d-auteur-adoptee-par-le-parlement-europeen_5441480_4408996.html")
txt = preprocess(txt)
txt2 = getText("https://www.lemonde.fr/societe/article/2019/03/26/manifestante-blessee-a-nice-les-versions-s-opposent_5441449_3224.html")
txt2 = preprocess(txt2)

queryE = expand_query(query)

corpus = [" ".join(queryE)," ".join(txt)," ".join(txt2)]
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(corpus).toarray()
print(matrix.shape)

mat = normalize(matrix)
query = mat[0]
doc = mat[1:mat.shape[0]]
print(np.dot(query,doc.transpose()))



