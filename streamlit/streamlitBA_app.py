import streamlit as st
import psycopg

def get_data(author):
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM btc_data WHERE author = %s", (author,))
    data = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return data
    

st.title("Bitcoin Information Center 🪙")

option = st.selectbox(
    "Which author would you like to read?",
    ("Denys Serhiichuk", "Arman Shirinyan", "Godfrey Benjamin"),
    index=None
)

st.write("You selected:", option)

if option is not None:
    data = get_data(option)
    st.dataframe(data)
