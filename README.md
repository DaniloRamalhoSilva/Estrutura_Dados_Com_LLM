# Mercado Livre Scraper API

Este projeto disponibiliza uma API simples que recebe uma URL de produto do Mercado Livre, realiza o scraping da página e retorna os dados estruturados em formato JSON. O processamento de dados utiliza um modelo da OpenAI para extrair informações relevantes do HTML.

## Instalação

```bash
pip install -r requirements.txt
```

É necessário definir a variável de ambiente `OPENAI_API_KEY` com sua chave de acesso.

## Execução

```bash
uvicorn api:app --reload
```

A API ficará disponível em `http://localhost:8000` e expõe o endpoint `/scrape` que recebe o parâmetro `url`.

Exemplo de requisição:

```
GET /scrape?url=https://produto.mercadolivre.com.br/...
```

## Funcionamento

1. O endpoint cria um driver Selenium em modo headless.
2. O driver navega até a URL informada e coleta os principais elementos da página.
3. O HTML obtido é enviado para o modelo de linguagem, que devolve os dados estruturados.
4. A resposta da API é um JSON com essas informações.
