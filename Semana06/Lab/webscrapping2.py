import requests
from bs4 import BeautifulSoup

my_url = 'http://www.feelt.ufu.br/acontece'
my_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63'}

page = requests.get(my_url, headers=my_header)
# print(page.content)

soup = BeautifulSoup(page.content, 'html5lib')
# print(soup.prettify())
# print(len(list(soup.children)))
html = list(soup.children)[1]
# print(html)
content = list(html.children)
# print(content[2])

atributos = {'class':'titulo'}
resultado = soup.find_all('h3',attrs=atributos)

for h3 in resultado:
    print(h3.get_text(),'\n')