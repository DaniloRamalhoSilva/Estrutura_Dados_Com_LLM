from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mercadolivre import scrap_product, scrap_comments_html, _validate_mercadolivre_url
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
    if not _validate_mercadolivre_url(url):
        raise HTTPException(status_code=400, detail="URL deve ser do Mercado Livre")

    driver = create_driver()
    try:
        _, raw_html = scrap_product(url, driver)
        comments_html = scrap_comments_html(url, 5, driver)
        raw_html += comments_html

        data = extract_structured(raw_html)

        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        driver.quit()
