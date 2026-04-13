import pandas as pd
import plotly.express as px
import sqlite3
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def query_to_df(sql: str):
    try:
        con = sqlite3.connect('ecommerce_sqlite.db')
        df = pd.read_sql_query(sql, con)
        con.close()
        return df
    except Exception as e:
        print(f'SQL error: {e}')
        return None

def pick_chart_type(question: str, columns: list) -> str:
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            # model="llama-3.3-70b-versatile"
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        prompt = f"""Question: {question}
Columns in result: {columns}

Reply with ONLY one word — the best chart type:
- bar: comparing categories or rankings
- line: trends over time (when there is a date/month column)
- pie: proportions or percentages
- scatter: relationship between two numbers
- none: single number or text result

One word only:"""
        response = llm.invoke(prompt)
        return response.content.strip().lower()
    except:
        return "bar"

def auto_chart(df, question: str):
    if df is None or df.empty:
        print("No data to chart")
        return None

    cols = df.columns.tolist()
    num_cols = df.select_dtypes('number').columns.tolist()
    cat_cols = df.select_dtypes('object').columns.tolist()

    print(f"Columns: {cols}")
    print(f"Numeric: {num_cols}")
    print(f"Categorical: {cat_cols}")

    chart_type = pick_chart_type(question, cols)
    print(f"Chart type: {chart_type}")

    if chart_type == 'pie' and len(cols) >= 2:
        label_col = cols[0]
        value_col = num_cols[0] if num_cols else cols[1]
        return px.pie(df, names=label_col, values=value_col, title=question)

    elif chart_type == 'line' and len(cols) >= 2:
        x_col = cols[0]
        y_col = num_cols[0] if num_cols else cols[1]
        return px.line(df, x=x_col, y=y_col, title=question,
                       color_discrete_sequence=['#534AB7'])

    elif chart_type == 'scatter' and len(num_cols) >= 2:
        return px.scatter(df, x=num_cols[0], y=num_cols[1], title=question,
                          color_discrete_sequence=['#534AB7'])

    elif chart_type == 'none':
        return None

    # bar is default
    if len(cols) >= 2:
        x_col = cat_cols[0] if cat_cols else cols[0]
        y_col = num_cols[0] if num_cols else cols[1]
        return px.bar(df, x=x_col, y=y_col, title=question,
                      color_discrete_sequence=['#1D9E75'])

    return None