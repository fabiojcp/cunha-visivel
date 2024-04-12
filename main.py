import os
import asyncio
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

if not os.path.exists("assets/pdf"):
    os.makedirs("assets/pdf")

async def wait_for_new_window(old_handles):
    while True:
        new_handles = driver.window_handles
        if len(new_handles) > len(old_handles):
            return new_handles
        await asyncio.sleep(1)

async def download_pdf(link):
    pdf_url = link.get_attribute('href')

    driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)

    new_handles = await wait_for_new_window(driver.window_handles)

    driver.switch_to.window(new_handles[-1])

    driver.find_element(By.ID, "download").click()

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

driver = webdriver.Chrome()

driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]')

tasks = [download_pdf(link) for link in links]

asyncio.run(asyncio.wait(tasks))

driver.quit()







