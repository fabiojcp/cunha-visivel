import random
import time
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class CunhaScraper:
    """
    Gets all PDF download links from the Cunha Imprensa Oficial website.
    """

    def __init__(
        self,
        cunha_imprensa_oficial_url: str = "https://www.imprensaoficialmunicipal.com.br/cunha",
        pdf_links_css_selector: str = 'a[href^="https://dosp.com.br/impressao.php?i="]',
        headful: bool = False,
    ):
        self.cunha_imprensa_oficial_url = cunha_imprensa_oficial_url
        self.pdf_links_css_selector = pdf_links_css_selector
        self.headful = headful

    def get_pdf_links(self) -> list[str]:
        """
        Get all PDF download links from the Cunha Imprensa Oficial website.
        """

        chrome_options = webdriver.ChromeOptions()

        if not self.headful:
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

        logger.info("Starting Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        logger.info("Chrome driver started.")

        pdf_links = []

        try:
            logger.info(f"Opening URL \"{self.cunha_imprensa_oficial_url}\"...")
            driver.get(self.cunha_imprensa_oficial_url)
            logger.info(f"Opened URL \"{self.cunha_imprensa_oficial_url}\".")

            while True:
                logger.info("Getting PDF links...")
                links = driver.find_elements(
                    By.CSS_SELECTOR, self.pdf_links_css_selector
                )
                logger.info(f"Got {len(links)} PDF links...")
                for link in links:
                    pdf_url = link.get_attribute("href")
                    if not pdf_url in pdf_links:
                        logger.info(f"Adding PDF link: {pdf_url}")
                        pdf_links.append(pdf_url)

                try:
                    logger.info("Clicking \"next\" button in the webpage...")
                    next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                    # sleep for a random short time to avoid being blocked
                    time.sleep(random.uniform(0.5, 1.5))
                    next_button.click()
                except NoSuchElementException:
                    logger.info("No more pages to scrape.")
                    break
        finally:
            driver.quit()
            logger.info("Chrome driver closed.")

        return pdf_links
