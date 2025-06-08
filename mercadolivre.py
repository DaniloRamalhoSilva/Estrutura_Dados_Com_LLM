from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementNotInteractableException

from database import save_url, save_review
import time

def scrap_list(produto, url, driver):
    try:
        driver.get(url)
        time.sleep(2)  # precisamos utilizar o sleep por 2 motivos: 1- Para não ser bloqueado; 2- Carregamentos dinâmicos que o Selenium não consegue recuperar
        print(driver.current_url)

        ol = driver.find_element(By.CSS_SELECTOR, "ol.ui-search-layout")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: ol.is_displayed())

        h3s = ol.find_elements(By.CSS_SELECTOR, "h3.poly-component__title-wrapper")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: h3s)

        print(f"Total de produtos encontrados: {len(h3s)}")

        for h3 in h3s:
            poduct_url = h3.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: wait)
            save_url(produto, poduct_url)
            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: url)

        next = driver.find_element(By.CSS_SELECTOR, ".andes-pagination__button--next a")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: next.is_displayed())

        if next:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", next)
            driver.execute_script("setTimeout(function() { document.querySelector('.andes-pagination__button--next a').click(); }, 3000);")

            time.sleep(4)
            current_url = driver.current_url
            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: current_url)

            return current_url

        return False

    except Exception as e:
        raise e

def scrap_product(url: str, driver):
    try:
        driver.get(url)
        time.sleep(3)  # aqui você pode trocar por WebDriverWait se preferir

        current_url = driver.current_url
        fragments = []

        # 1) meta og:title
        try:
            meta = driver.find_element(By.XPATH, "//meta[@property='og:title']")
            fragments.append(meta.get_attribute("outerHTML"))
        except NoSuchElementException:
            pass

        # 2) reviews header
        try:
            reviews = driver.find_element(By.CSS_SELECTOR, "h2.ui-review-capability__header__title")
            fragments.append(reviews.get_attribute("outerHTML"))
        except NoSuchElementException:
            pass

        # 3) seller info
        try:
            seller = driver.find_element(By.CSS_SELECTOR, "div.ui-seller-data-header__title-container")
            fragments.append(seller.get_attribute("outerHTML"))
        except NoSuchElementException:
            pass

        # 4) descrição do produto
        # opcional: via JS para já obter o HTML
        desc_html = driver.execute_script(
            "var el = document.querySelector('p.ui-pdp-description__content');"
            "return el ? el.outerHTML : '';"
        )
        if desc_html:
            fragments.append(desc_html)

        # 5) montar container único
        raw_html = (
            "<div class='scrap-container'>\n" +
            "\n".join(fragments) +
            "\n</div>"
        )

        return current_url, raw_html

    except Exception as e:
        print(f"[scrap_product] erro em {url}: {e}")
        raise

def scrap_comments(id, url, limit, driver):
    try:
        driver.get(url)
        time.sleep(3)
        driver.implicitly_wait(10)

        # 1) Tentar clicar no "mostrar mais"
        try:
            btn = driver.find_element(By.CSS_SELECTOR, "button.show-more-click")
            btn.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        # 2) Se existe iframe de reviews, entrar nele
        try:
            iframe = driver.find_element(By.CSS_SELECTOR, "#ui-pdp-iframe-reviews")
            driver.switch_to.frame(iframe)
            time.sleep(1)
        except NoSuchElementException:
            pass

        # 3) Coletar comentários (até o limite)
        comments_html = ""
        comments = driver.find_elements(By.CSS_SELECTOR, 'article.ui-review-capability-comments__comment')
        for c in comments[:limit]:
            try:
                content_p = c.find_element(By.CSS_SELECTOR,'p.ui-review-capability-comments__comment__content')
                comments_html += content_p.get_attribute("outerHTML")
            except NoSuchElementException:
                continue

        # 4) Envolver tudo num container e salvar
        wrapped = f"<div class='scrap-container'>{comments_html}</div>"
        save_review(id, wrapped)

        # 5) Voltar para o contexto principal (fora do iframe)
        driver.switch_to.default_content()

    except Exception as e:
        print("Erro em scrap_comments:", e)

