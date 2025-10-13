import streamlit as st   
import psycopg


def get_data(city):
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM weather_data WHERE city = %s", (city,))
    data = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return data
    

st.badge("Hello World!!!!!!", icon="🍉", color="violet")

option = st.selectbox(
    "Which city would you like to know the weather for?",
    ("Berlin", "Sydney", "Tokyo"),
    index=None
)

st.write("You selected:", option)

if option != None:
    data = get_data(option)
    st.dataframe(data)
    
    #build plot with data