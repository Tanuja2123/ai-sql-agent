# AI SQL Agent

Ask questions about your data in plain English and get instant answers with charts.

Built with LangChain, Groq (Llama 3), DuckDB, Plotly, and Streamlit. 100% free to run.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![LangChain](https://img.shields.io/badge/LangChain-latest-green) ![Groq](https://img.shields.io/badge/Groq-Free-orange)

---

## What it does

Type any question in plain English. The AI figures out the correct SQL, runs it against the database, and returns the answer with an auto-generated chart.

**Example questions:**
- *Top 5 products by revenue?*
- *Show me the trend of total sales amount over each month*
- *What is the distribution of orders by status?*
- *Show relationship between price and stock in products*
- *Which city has the most customers?*

---

## Features

- **Natural language to SQL** — ask anything, the agent writes the SQL automatically
- **Smart chart selection** — LLM picks the best chart type (bar, line, pie, scatter) based on your question
- **CSV upload** — upload your own CSV and query it instantly
- **Auto insights** — one-click anomaly detection, revenue summary, and opportunity finder
- **Query history** — past queries saved to disk, persist across sessions
- **PDF export** — export your full session as a formatted PDF report
- **Download CSV** — download query results as CSV with one click
- **Schema-aware agent** — agent understands table relationships for accurate SQL

---

## Tech stack

| Tool | Purpose |
|------|---------|
| LangChain | SQL agent framework |
| Groq (Llama 3.1) | LLM — free, fast inference |
| DuckDB | Primary database |
| SQLite | Query layer for LangChain |
| Plotly | Interactive charts |
| Streamlit | Web UI |
| ReportLab | PDF export |

---

## Project structure

```
ai-sql-agent/
├── app.py               # Streamlit UI
├── agent.py             # LangChain SQL agent + Groq LLM
├── db_setup.py          # Creates DuckDB database with sample data
├── reset_db.py          # Exports DuckDB to SQLite for LangChain
├── requirements.txt     # All dependencies
├── .env                 # Your Groq API key (never commit this)
├── ecommerce.db         # DuckDB database (auto-created)
├── ecommerce_sqlite.db  # SQLite database (auto-created)
├── query_history.json   # Saved query history (auto-created)
└── utils/
    ├── __init__.py
    ├── visualizer.py    # Chart logic + SQL extraction
    ├── history.py       # Query history save/load
    └── pdf_export.py    # PDF report generation
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ai-sql-agent.git
cd ai-sql-agent
```

### 2. Install dependencies

```bash
pip install langchain langchain-groq langchain-community
pip install duckdb streamlit plotly pandas
pip install python-dotenv reportlab
```

### 3. Get your free Groq API key

- Go to [console.groq.com](https://console.groq.com)
- Sign up for free (no credit card needed)
- Create an API key
- Create a `.env` file in the project root:

```
GROQ_API_KEY=gsk_your_key_here
```

### 4. Run the app

```bash
python db_setup.py
python reset_db.py
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Running again after closing

Every time you reopen the project, just run these 3 commands:

```bash
python db_setup.py
python reset_db.py
streamlit run app.py
```

---

## Database schema

The default database is a sample e-commerce dataset with 3 tables:

**products** — 10 products across 5 categories
| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary key |
| name | VARCHAR | Product name |
| category | VARCHAR | Electronics, Clothing, Books, Home, Sports |
| price | FLOAT | Price in rupees |
| stock | INTEGER | Units available |

**customers** — 50 customers across 6 cities
| Column | Type | Description |
|--------|------|-------------|
| customer_id | INTEGER | Primary key |
| name | VARCHAR | Customer name |
| city | VARCHAR | Mumbai, Delhi, Bangalore, Chennai, Pune, Hyderabad |
| signup_date | DATE | Registration date |

**orders** — 500 orders
| Column | Type | Description |
|--------|------|-------------|
| order_id | INTEGER | Primary key |
| customer_id | INTEGER | Foreign key → customers |
| product_id | INTEGER | Foreign key → products |
| quantity | INTEGER | Units ordered |
| amount | FLOAT | Total amount paid |
| order_date | DATE | Order date |
| status | VARCHAR | delivered / shipped / cancelled / processing |

---

## Using your own data

Upload any CSV file using the **Upload your own data** section in the sidebar. The file is automatically loaded as a new table in the database and the agent can query it immediately.

> Note: Files named `orders.csv`, `products.csv`, or `customers.csv` are automatically renamed to `uploaded_orders`, `uploaded_products`, `uploaded_customers` to protect the original tables.

---

## Example questions by chart type

| Chart | Example question |
|-------|-----------------|
| Bar | `How many customers are there in each city?` |
| Bar | `Top 5 products by revenue?` |
| Pie | `What is the distribution of orders by status?` |
| Pie | `Show me the share of revenue by category` |
| Line | `Show me the trend of total sales amount over each month` |
| Line | `Show me the trend of order count over each month` |
| Scatter | `Show relationship between quantity and amount in orders` |
| Scatter | `Plot price vs stock for all products` |

---

## Troubleshooting

**Rate limit error** — Groq free tier has a daily token limit. Wait a few minutes and try again, or switch to a smaller model in `agent.py`.

**Model decommissioned error** — Groq occasionally retires models. Change the model name in `agent.py` and `utils/visualizer.py` to `llama-3.1-8b-instant`.

**Database error after CSV upload** — Run `python reset_db.py` to restore the original database, then restart Streamlit.

**Corrupted history file** — Delete `query_history.json` and restart Streamlit.

**Blank page on startup** — Wait 10-15 seconds for the LLM to initialise. Check the terminal for errors.

---

## How it works

```
User question
     ↓
LangChain SQL Agent
     ↓
Groq LLM reads schema → writes SQL → executes → returns answer
     ↓
Separate LLM call generates chart SQL
     ↓
Second LLM call picks chart type (bar/line/pie/scatter)
     ↓
Plotly renders chart
     ↓
Streamlit displays answer + chart + raw data
```

---

## What I learned building this

- Agentic tool-use patterns with LangChain
- Why `temperature=0` is critical for SQL generation
- Hybrid approach: agent for natural language answers, direct LLM call for chart SQL
- DuckDB vs SQLite tradeoffs for analytical workloads
- Prompt engineering for structured outputs (chart type selection)
- Streamlit session state management for chat interfaces

---

## License

MIT — free to use and modify.
