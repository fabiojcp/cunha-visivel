import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


if not os.path.exists("assets/pdf"):
    os.makedirs("assets/pdf")

log_filename = "./assets/download_log.txt"

if not os.path.exists(log_filename):
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write("Logs\n\n")


def already_downloaded(pdf_url: str) -> bool:
    with open(log_filename, "r", encoding="utf-8") as f:
        return f.read().find(pdf_url) != -1


def extract_filename_from_url(pdf_url: str) -> None:
    filename = max(
        ["./assets/pdf/" + f for f in os.listdir("./assets/pdf/")], key=os.path.getctime
    )
    filename = re.sub(r"\.crdownload$", "", filename)
    filename = re.sub(r"\./assets/pdf/", "", filename)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"Nome do arquivo: {filename}\n")
        log_file.write(f"Link: {pdf_url}\n\n")


def download_pdf(pdf_url: str, driver: WebDriver) -> None:
    driver.execute_script("window.open(arguments[0], '_blank');", pdf_url)
    time.sleep(1)

    new_handles = driver.window_handles
    driver.switch_to.window(new_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "./assets/pdf",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

    while True:
        links = driver.find_elements(
            By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]'
        )
        for link in links:
            pdf_url = link.get_attribute("href")

            if not already_downloaded(pdf_url):
                download_pdf(pdf_url, driver)
                extract_filename_from_url(pdf_url)

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
            next_button.click()
            time.sleep(2)
        except NoSuchElementException:
            break

finally:
    driver.quit()
