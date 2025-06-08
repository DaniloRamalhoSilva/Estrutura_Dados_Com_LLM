import sqlite3

def create_db():
    """
    Cria o banco de dados SQLite com três tabelas:
    - products_url: Armazena URLs de produtos para scraping
    - products_data: Armazena dados gerais dos produtos
    - products_review: Armazena avaliações dos produtos
    - products_html_raw Armazena HTML bruto
    - products_structured_llm Armazena dados estruturados extraídos de uma ferramenta de LLM
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_url (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            url TEXT,                
            scraped INTEGER DEFAULT 0,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            products_url_id INTEGER,
            
            url TEXT,
            title TEXT,
            price REAL,
            review_rating REAL,
            review_amount INTEGER,
            seller TEXT,
            description TEXT,            
            brand TEXT,
            model TEXT,
            color TEXT,
            description_quality TEXT,
            comments_quality TEXT,
            review_count INTEGER,
            photo_count INTEGER,
            confidence_rating TEXT,                
            
            raw_html TEXT,
            comments_html TEXT,
            
            comments_scraped INTEGER DEFAULT 0,    
            processed INTEGER DEFAULT 0,  
            label TEXT DEFAULT NULL    
        )
    """)
    conn.commit()

    conn.close()


def save_url(produto, url):
    """
    Salva um novo produto e sua URL na tabela products_url.

    Args:
        produto (str): Nome do produto
        url (str): URL do produto no Mercado Livre
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_url (produto, url) VALUES (?, ?)", (produto, url))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_product(products_url_id, url, raw_html):
    """
    Salva os dados de um produto na tabela products_data.

    Args:
        product_url_id (id): id da tabela products_url
        url (str): URL do produto
        raw_html (TEXT): Elementos principais para aextração dos dados
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_data (products_url_id, url, raw_html)"
                    "values (?, ?, ?) ",
            (products_url_id, url, raw_html))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()


def query(sql):
    """
    Executa uma consulta SQL personalizada no banco de dados.

    Args:
        sql (str): Query SQL a ser executada

    Returns:
        list: Resultado da consulta em forma de lista
    """
    conn = sqlite3.connect("mercadolivre.db")
    try:
        query = sql.split(' ')
        cur = conn.cursor()
        cur.execute(sql)

        if query[0].lower() == "select":
            return cur.fetchall()
        else:
            conn.commit()
            return True

    except Exception as e:
      print(f"Erro ao tentar executar a query: {e}")
    finally:
        conn.close()
