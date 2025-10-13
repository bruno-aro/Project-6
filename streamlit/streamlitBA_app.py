import streamlit as st
import psycopg

st.title("🟠 BTC News")

def get_btc(author=None):
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)

 cur.execute("SELECT * FROM btc_data WHERE author = %s", (author,))
        data = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return data

author = st.selectbox(
    "Filter by author (optional):",
    options=[None, "Alex Dovbnya", "Denys Serhiiichuk", "Arman Shirinyan"],
    index=0
)

df = get_btc(author)
st.dataframe(df, use_container_width=True)