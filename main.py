import os
import asyncio
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Verificar se o diretório "assets/pdf" existe e criá-lo se não existir
if not os.path.exists("assets/pdf"):
    os.makedirs("assets/pdf")

# Função para esperar até que o número de janelas seja atualizado
async def wait_for_new_window(old_handles):
    while True:
        new_handles = driver.window_handles
        if len(new_handles) > len(old_handles):
            return new_handles
        await asyncio.sleep(1)

# Função para baixar o PDF
async def download_pdf(link):
    # Obter o URL do link
    pdf_url = link.get_attribute('href')

    # Abrir o link em uma nova janela
    driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)

    # Esperar até que uma nova janela seja aberta
    new_handles = await wait_for_new_window(driver.window_handles)

    # Mudar o foco para a nova janela
    driver.switch_to.window(new_handles[-1])

    # Baixar o PDF
    driver.find_element(By.ID, "download").click()

    # Fechar a nova janela
    driver.close()

    # Voltar ao foco na janela principal
    driver.switch_to.window(driver.window_handles[0])

# Inicialize o driver do Selenium
driver = webdriver.Chrome()

# Carregar a página
driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

# Encontrar todos os links na página que começam com o prefixo desejado
links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]')

# Criar uma lista de tarefas assíncronas para baixar cada PDF
tasks = [download_pdf(link) for link in links]

# Executar as tarefas assíncronas
asyncio.run(asyncio.wait(tasks))

# Fechar o navegador
driver.quit()



# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # Inicialize o driver do Selenium (certifique-se de ter o WebDriver instalado e no PATH)
# driver = webdriver.Chrome()

# # Carregue a página
# driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

# # Encontre todos os links na página que começam com o prefixo desejado
# links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]')

# # Imprima os links encontrados
# for link in links:
#     parent_li = link.find_element(By.XPATH, '..')
#     h3_text = parent_li.find_element(By.CSS_SELECTOR, 'a:first-child h3').text
#     print(link.get_attribute('href'), h3_text)

# # Feche o navegador
# driver.quit()