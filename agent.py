from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLDatabase.from_uri("sqlite:///ecommerce_sqlite.db")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    # "llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

SCHEMA_CONTEXT = """You are a data analyst assistant for an e-commerce company.

Database tables:
- products: product_id (PK), name, category, price (in rupees), stock (units available)
- customers: customer_id (PK), name, city, signup_date
- orders: order_id (PK), customer_id (FK), product_id (FK), quantity, amount (total paid), order_date, status (delivered/shipped/cancelled/processing)

Key rules:
- Revenue = SUM(amount), never SUM(quantity * price)
- Always exclude cancelled orders when calculating revenue
- For monthly trends use strftime('%Y-%m', order_date) as month
- orders.product_id joins to products.product_id
- orders.customer_id joins to customers.customer_id
"""

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    prefix=SCHEMA_CONTEXT
)

def run_query(question: str) -> str:
    try:
        result = agent.invoke({"input": question})
        return result["output"]
    except Exception as e:
        if "rate_limit" in str(e).lower() or "429" in str(e):
            return "Rate limit reached. Please wait a few minutes and try again."
        return "Answer"
        # return "I could not answer that question. Please try rephrasing it."

def get_sql_for_chart(question: str) -> str:
    try:
        prompt = f"""You are a SQL expert. Write a single SQLite query to answer this question.

Tables available:
- products (product_id, name, category, price, stock)
- customers (customer_id, name, city, signup_date)
- orders (order_id, customer_id, product_id, quantity, amount, order_date, status)

Question: {question}

Rules:
- Return ONLY the SQL query, nothing else
- No markdown, no backticks, no explanation
- No semicolon at the end
- Maximum 20 rows in result
- Always include a GROUP BY if aggregating
- For time trends use strftime('%Y-%m', order_date) as month

SQL:"""
        response = llm.invoke(prompt)
        return response.content.strip()
    except:
        return None