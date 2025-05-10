import time
import zipfile
import os
from playwright.sync_api import sync_playwright

download_path = r"C:\Users\Grory\OneDrive\Área de Trabalho\igor"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) 
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    page.goto("https://www.telecocare.com.br/mapaerbs/")

    with page.expect_download() as download_info:
        page.locator("text=Clique aqui").click()
    download = download_info.value

    zip_file_path = os.path.join(download_path, download.suggested_filename)
    download.save_as(zip_file_path)

    time.sleep(3) 

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(download_path) 

    for file in os.listdir(download_path):
        if file.endswith(".xlsx"):
            xlsx_file_path = os.path.join(download_path, file)

    browser.close()


// esse código não esta funcionando pois o site "https://www.telecocare.com.br/mapaerbs/" esta fora temporariamente...
