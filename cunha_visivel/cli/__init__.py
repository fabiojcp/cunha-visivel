import click



# create a click cli command to download the pdfs
@click.command()
@click.option("--headful", is_flag=True, help="Run the browser in headful mode")
def cunha_cli(headful: bool) -> None:
    print("Fabão")
    # chrome_options = webdriver.ChromeOptions()
    
    # if not headful:
    #     chrome_options.add_argument("--headless")

    # chrome_options.add_experimental_option(
    #     "prefs",
    #     {
    #         "download.default_directory": "./assets/pdf",
    #         "download.prompt_for_download": False,
    #         "download.directory_upgrade": True,
    #         "safebrowsing.enabled": True,
    #     },
    # )

    # driver = webdriver.Chrome(options=chrome_options)

    # try:
    #     driver.get("https://www.imprensaoficialmunicipal.com.br/cunha")

    #     while True:
    #         links = driver.find_elements(
    #             By.CSS_SELECTOR, 'a[href^="https://dosp.com.br/impressao.php?i="]'
    #         )
    #         for link in links:
    #             pdf_url = link.get_attribute("href")

    #             if not already_downloaded(pdf_url):
    #                 download_pdf(pdf_url, driver)
    #                 extract_filename_from_url(pdf_url)

    #         try:
    #             next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
    #             next_button.click()
    #         except NoSuchElementException:
    #             break
    # finally:
    #     driver.quit()

