import os
import json
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


# 1) Configure sua API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você recebe o HTML bruto de uma página de anúncio de cartucho HP. Retorne um JSON com os campos:
- titulo: ()
- marca: (ex: HP)
- modelo: (ex: 667)  media de preço do modelo 667 é 150,50
- preco: número (ex: 120,00)
- cor: (ex: preto, colorido)
- qualidade_descricao: breve avaliação da clareza/ortografia do texto (ex: \"boa\", \"média\", \"ruim\")
- qualidade_comentarios: breve avaliação de sentimento dos clientes baseado nos comentarios. (ex: \"Satisfeitos\", \"Indiferentes\", \"Insatisfeitos\")
- avaliação_revisao: decimal
- valor_revisao: inteiro 
- vendedor: nome da loja ou responsavel pela venda
- quantidade_reviews: inteiro
- quantidade_fotos: inteiro
- classificacao_confianca: procure elementos que possam identificar se o produto é (ex: \"Original\", \"Pirata\", \"Suspeito\")
- percentagem: porcentagem de confiança de o produto ser original
- justificativa: texto curto descrevendo os critérios usados para a classificação
Responda **somente** com um JSON válido.
"""

def extract_structured(html: str) -> dict:

    res = client.responses.create(
        model="gpt-4o-mini",
        instructions=(
            SYSTEM_PROMPT  
        ),
        input=html  
    )
    content = res.output_text.strip().lower()
    
    # Remove blocos markdown
    if content.startswith("```json"):
        content = content.replace("```json", "").strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    return json.loads(content)

def process_all_html():
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()

    # busca todas as páginas ainda não processadas
    cur.execute("""
        SELECT id, raw_html, comments_html
          FROM products_data 
         WHERE processed = 0    
    """)
    rows = cur.fetchall()

    for pdid, raw_html, comments_html in rows:
        try:
            # garante que comments_html é string
            comments_html = comments_html or ""
            html = raw_html + comments_html
            data = extract_structured(html)

            # atualiza na tabela estruturada
            cur.execute("""
                UPDATE products_data
                SET
                    title               = ?,
                    brand               = ?,
                    model               = ?,
                    price               = ?,
                    color               = ?,
                    description_quality = ?,
                    comments_quality    = ?,
                    review_rating       = ?,
                    review_amount       = ?,
                    seller              = ?,
                    review_count        = ?,
                    photo_count         = ?,
                    confidence_rating   = ?,
                    processed           = ?
                WHERE
                    id    = ?
            """, (
                data.get("titulo"),
                data.get("marca"),
                data.get("modelo"),
                data.get("preco"),
                data.get("cor"),
                data.get("qualidade_descricao"),
                data.get("qualidade_comentarios"),
                data.get("avaliação_revisao"),
                data.get("valor_revisao"),
                data.get("vendedor"),
                data.get("quantidade_reviews"),
                data.get("quantidade_fotos"),
                data.get("classificacao_confianca"),
                1,
                pdid
            ))
            conn.commit()
        except Exception as e:
            print(f"Erro ao processar HTML {pdid}: {e}")

    # exporta CSV com tudo que foi extraído
    df = pd.read_sql("""
        SELECT title, brand, model, price, color, description_quality, comments_quality,
               review_rating, review_amount, seller, review_count, photo_count, confidence_rating,processed           
          FROM products_data 
    """, conn)
    df.to_csv("data\structured_data.csv", index=False, sep=";")

    conn.close()

