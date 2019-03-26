import re


def clean_html(html_txt):
    mystr = html_txt
    # On parse le html

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(mystr, 'html.parser')

    txt = [re.sub(' +',' ',(''.join(node.findAll(text=True))).replace("\t", " ").replace("\r\n",".")) for node in soup.findAll('p')]
    txt = ".".join([stri.replace("\n", "") for stri in txt])
    return(txt)