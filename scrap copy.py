# from bs4 import BeautifulSoup
# import requests

# html = requests.get("https://www.imprensaoficialmunicipal.com.br/cunha").content

# soup = BeautifulSoup(html, 'html.parser')

# # Encontrar todos os links
# links = soup.find_all('a')

# # Filtrar apenas os links que têm o atributo href e começam com o prefixo desejado
# filtered_links = [link['href'] for link in links if link.has_attr('href') and link['href'].startswith('https://dosp.com.br/exibe_do.php?i=')]

# # Imprimir os links filtrados
# for link in filtered_links:
#     print(link)

from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicialize o driver do Selenium (certifique-se de ter o WebDriver instalado e no PATH)
driver = webdriver.Chrome()

# Carregue a página
driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

# Encontre todos os links na página que começam com o prefixo desejado
links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]')

# Imprima os links encontrados
for link in links:
    print(link.get_attribute('href'))

# Feche o navegador
driver.quit()