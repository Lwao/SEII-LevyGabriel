from bs4 import BeautifulSoup
from urllib.request import urlopen

url1 = 'http://www.google.com'
url2 = 'http://www.wikipedia.org/'
url3 = 'http://en.wikipedia.org/wiki/Main_Page'

url = url3

with urlopen(url) as response:
    soup = BeautifulSoup(response, 'html.parser')

    for links in soup.find_all('a'):
        print('-> ', links.get('href', '/'))