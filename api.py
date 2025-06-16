from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mercadolivre import scrap_product
from structuring_llm import extract_structured

app = FastAPI()


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


@app.get("/scrape")
def scrape(url: str):
    """Scrapes a Mercado Livre product page and returns structured data."""
    driver = create_driver()
    try:
        _, raw_html = scrap_product(url, driver)
        data = extract_structured(raw_html)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        driver.quit()
