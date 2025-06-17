# Mercado Livre Scraper API 🕵️‍♂️📦

Projeto robusto desenvolvido em Python que realiza coleta e análise inteligente de anúncios do Mercado Livre, utilizando tecnologias modernas como Selenium, FastAPI e integração com a API da OpenAI. A API exposta permite extrair informações detalhadas e estruturadas de qualquer anúncio do Mercado Livre de forma simples e rápida.

---

## 📚 Índice

- [Visão Geral](#visão-geral)
- [Recursos Principais](#recursos-principais)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura da API](#estrutura-da-api)
- [Front-end Relacionado](#front-end-relacionado)
- [Autores](#autores)

---

## 📝 Visão Geral

O projeto utiliza tecnologias avançadas para extrair e padronizar dados essenciais dos anúncios, oferecendo insights rápidos e precisos sobre a originalidade dos produtos anunciados.

### Fluxo do processo:

- **🕷️ Scraping**: Extração automática dos detalhes do anúncio e comentários através do Selenium.
- **🤖 Análise Inteligente**: Utilização da API OpenAI para estruturar e analisar o conteúdo coletado.
- **⚡ API FastAPI**: Disponibilização dos resultados via endpoint intuitivo.

---

## ✨ Recursos Principais

- ✅ Scraping eficiente e robusto com Selenium.
- 🤖 Processamento avançado dos dados utilizando LLM da OpenAI.
- 🌐 API rápida e intuitiva com FastAPI.
- 📦 Retorno estruturado em JSON com dados completos do anúncio.

---

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado
- Variável de ambiente configurada:
  - `OPENAI_API_KEY`

---

## 🛠️ Instalação

Clone e instale as dependências:

```bash
git clone https://github.com/seu-usuario/mercado_livre_scraper.git
cd mercado_livre_scraper
pip install -r requirements.txt
```

---

## 🚀 Como Usar

Inicie o servidor localmente:

```bash
uvicorn api:app --reload
```

A API estará disponível em:

```
http://localhost:8000
```

### 🔗 Endpoint `/scrape`

Faça uma requisição GET fornecendo a URL do anúncio:

```bash
GET /scrape?url=https://produto.mercadolivre.com.br/...
```

A resposta será um JSON detalhado contendo:

- Informações do anúncio
- Análise dos comentários
- Classificação de originalidade

---

## 💻 Estrutura da API

```text
api/
├── main.py
├── scraper/
│   ├── scraping.py
│   ├── openai_analysis.py
│   └── models.py
└── requirements.txt
```

---

## 🌐 Front-end Relacionado

O front-end que consome esta API está disponível no repositório:

- [Validador de Produtos HP](https://github.com/DaniloRamalhoSilva/Projeto_HP)

---

## 👨‍🏫 Autores

- Danilo Ramalho Silva | RM: 555183
- Israel Dalcin Alves Diniz | RM: 554668
- João Vitor Pires da Silva | RM: 556213
- Matheus Hungaro | RM: 555677
- Pablo Menezes Barreto | RM: 556389
- Tiago Toshio Kumagai Gibo | RM: 556984

---

## 📜 Licença

Projeto licenciado sob a **MIT License**. Consulte o arquivo `LICENSE` para mais detalhes.

