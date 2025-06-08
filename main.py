from database import save_product
from mercadolivre import scrap_list, scrap_product, scrap_comments
from structuring_llm import process_all_html

from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options

import time, random
import database

def list(produto, driver, limit = 5):
    url = f"https://lista.mercadolivre.com.br/{quote(produto)}"
    page = scrap_list(produto, url, driver)

    counter = 0
    while page and counter < limit:
        counter = counter + 1
        page = scrap_list(produto, page, driver)
        time.sleep(random.uniform(2.0, 3.0))  # para evitar ser identificado como scrap]

def product(driver, limit = 10):
    products_url = database.query(f"select * from products_url limit {limit}")

    for product_url in products_url:
        try:
            print(product_url[2])
            url, raw_html = scrap_product(product_url[2], driver)
            save_product(product_url[0], url, raw_html)
            database.query(f"update products_url set scraped = 1 where id = {product_url[0]}")
        except Exception as e:
            print(e)
            continue

def comments(driver, limit = None, comments_limit = 0):
    if limit:
        limit = f"limit {limit}"

    products_data = database.query(f"select * from products_data {limit}")
    for product_data in products_data:
        print(product_data[2])
        scrap_comments(product_data[0], product_data[3], comments_limit, driver)
        database.query(f"update products_data set comments_scraped = 1 where id = {product_data[0]}")


if __name__ == "__main__":
    # criando tabelas caso não existam
    database.create_db()

    #criando driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    # vamos começar recuperando a lista de produtos
    produto = "cartucho hp" #"cartucho hp original"

    # Limites de busca
    paginas = 1
    produtos = 10
    comentarios = 10

    # scraping
    list(produto, driver, paginas)
    product(driver, produtos)
    comments(driver, produtos, comentarios)

    # Processa html para extrair os dados extruturados com LLM
    process_all_html()  

    #driver.quit()
