import streamlit as st
import psycopg2
import pandas as pd

st.title("🟠 BTC News")

def get_btc(author=None):
    dbconn = st.secrets["DBCONN"]
    conn = psycopg2.connect(dbconn)

    if author:
        sql = """
            SELECT id, title, author, published_at
            FROM btc_data
            WHERE author = %s
            ORDER BY published_at DESC;
        """
        df = pd.read_sql(sql, conn, params=(author,))
    else:
        sql = """
            SELECT id, title, author, published_at
            FROM btc_data
            ORDER BY published_at DESC;
        """
        df = pd.read_sql(sql, conn)

    conn.close()
    # make sure datetime is parsed nicely
    if "published_at" in df:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    return df

# optional simple filter (can be None)
author = st.selectbox(
    "Filter by author (optional):",
    options=[None, "Alex Dovbnya", "Denys Serhiiichuk", "Arman Shirinyan"],
    index=0
)

df = get_btc(author)
st.dataframe(df, use_container_width=True)