# from bs4 import BeautifulSoup
# import requests

# html = requests.get("https://www.imprensaoficialmunicipal.com.br/cunha").content

# soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

from bs4 import BeautifulSoup
import requests

html = requests.get("https://www.imprensaoficialmunicipal.com.br/cunha").content

soup = BeautifulSoup(html, 'html.parser')

# Encontrar todos os elementos <a> com href começando com "https://dosp.com.br/impressao.php?i="
links = soup.find_all('a', href=lambda href: href and href.startswith('https://dosp.com.br/impressao.php?i='))

# Imprimir os links encontrados
for link in links:
    print(link['href'])