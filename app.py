

import streamlit as st
from agent import run_query, get_sql_for_chart
from utils.visualizer import query_to_df, auto_chart
from utils.history import load_history, save_query, clear_history
from utils.pdf_export import export_session_pdf

st.set_page_config(
    page_title="AI SQL Agent",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.title("AI SQL Agent")
    st.caption("Ask questions in plain English.")
    st.divider()

    st.subheader("Available tables")
    st.code("products\ncustomers\norders")

    st.divider()
    st.subheader("Past queries")
    past = load_history()
    if past:
        for item in reversed(past[-5:]):
            with st.expander(item['timestamp'] + ' — ' + item['question'][:35]):
                st.write(item['answer'])
                if item['sql']:
                    st.code(item['sql'], language='sql')
        if st.button("Clear history", use_container_width=True):
            clear_history()
            st.rerun()
    else:
        st.caption("No past queries yet.")

    if st.session_state.get("history"):
        st.divider()
        pdf_bytes = export_session_pdf(st.session_state["history"])
        st.download_button(
            label="Export session as PDF",
            data=pdf_bytes,
            file_name="sql_agent_report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="pdf_export"
        )

    st.divider()
    st.subheader("Auto insights")

    if st.button("Find anomalies", use_container_width=True):
        st.session_state["auto_query"] = (
            "Compare total orders and revenue this month vs last month. "
            "Flag any products, categories, or customers that show unusual "
            "changes more than 20% difference. List specific numbers."
        )
    if st.button("Top opportunities", use_container_width=True):
        st.session_state["auto_query"] = (
            "Which products have high stock but low sales? "
            "Which cities have few customers but high order values? "
            "Give 3 specific business recommendations."
        )
    if st.button("Revenue summary", use_container_width=True):
        st.session_state["auto_query"] = (
            "Give a complete revenue summary: total revenue, "
            "top 3 products, top 3 cities, busiest month, "
            "and percentage of delivered vs cancelled orders."
        )

    st.divider()
    st.subheader("Example questions")
    examples = [
        "Top 5 products by revenue?",
        "What is the distribution of orders by status?",
        "Show me the trend of total sales amount over each month",
        "How many customers are there in each city?",
        "Show relationship between quantity and amount in orders",
        "Plot price vs stock for all products",
        "Show me the share of revenue by category",
        "Revenue by product category?",
        "How many orders were delivered vs cancelled?",
        "Show me the trend of order count over each month",
        "Which product has the lowest stock?",
        "Break down customers by city as percentages",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["auto_query"] = ex

    st.divider()
    st.subheader("Upload your own data")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        import pandas as pd
        import sqlite3
        import re

        df_upload = pd.read_csv(uploaded_file)
        raw_name = uploaded_file.name.replace(".csv", "")
        table_name = re.sub(r"[^a-zA-Z0-9_]", "_", raw_name).lower()

        protected = ["orders", "products", "customers"]
        if table_name in protected:
            table_name = "uploaded_" + table_name

        con = sqlite3.connect("ecommerce_sqlite.db")
        df_upload.to_sql(table_name, con, if_exists="replace", index=False)
        con.close()

        st.success(f"Table `{table_name}` loaded! ({len(df_upload)} rows)")
        st.caption("Columns: " + ", ".join(df_upload.columns.tolist()))
        st.info(f"Try asking: What are the top rows in {table_name}?")

st.title("AI SQL Agent")
st.write("Ask any question about the e-commerce data in plain English.")

if "history" not in st.session_state:
    st.session_state.history = []

auto_q = st.session_state.pop("auto_query", None)
question = st.chat_input("e.g. What are the top 5 products by revenue?")

if auto_q:
    question = auto_q

if question:
    try:
        with st.spinner("Thinking..."):
            answer = run_query(question)
            sql    = get_sql_for_chart(question)
            print(f"Chart SQL: {sql}")
            df     = query_to_df(sql) if sql else None
            fig    = auto_chart(df, question) if df is not None else None
            save_query(question, answer, sql)

        st.session_state.history.append({
            "q": question, "a": answer,
            "sql": sql, "fig": fig, "df": df
        })

    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            st.warning("Rate limit reached. Please wait a few minutes and try again.")
        elif "decommissioned" in error_msg.lower():
            st.warning("Model error — check your model name in agent.py.")
        else:
            st.warning(f"Something went wrong: {error_msg[:200]}")

for i, item in enumerate(reversed(st.session_state.history)):
    with st.chat_message("user"):
        st.write(item["q"])

    with st.chat_message("assistant"):
        st.write(item["a"])

        if item.get("sql"):
            with st.expander("View SQL query"):
                st.code(item["sql"], language="sql")

        if item.get("fig"):
            st.plotly_chart(item["fig"], use_container_width=True)

        if item.get("df") is not None:
            with st.expander("View raw data"):
                st.dataframe(item["df"], use_container_width=True)

        if item.get("df") is not None:
            csv = item["df"].to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="query_result.csv",
                mime="text/csv",
                key=f"download_{i}"
            )