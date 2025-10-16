import streamlit as st
import pandas as pd
import psycopg
import altair as alt
import google.generativeai as genai
import os

# --- Page setup ---
st.set_page_config(page_title="BTC Today", page_icon="🪙", layout="wide")
st.title("🪙 Bitcoin Today")

st.write("") 

st.markdown("""
💡 **About this page**  
Welcome to the **Bitcoin Today** — your gateway to the latest insights, articles, and analysis about Bitcoin. Browse curated news and publications 
from different authors to stay updated on **market trends**, **innovations**, and **expert opinions**. Select an author from the list to explore their latest 
contributions and dive deeper into the world of cryptocurrency.
""")

st.write("") 
st.write("") 

st.subheader("💵 Bitcoin Price (USD)")

# --- Load data from Supabase ---
@st.cache_data(ttl=1800)
def load_data():
    conn = psycopg.connect(st.secrets["DBCONN"])
    with conn.cursor() as cur:
        cur.execute("""
            SELECT trade_date, open, high, low, close, volume
            FROM alpha_vantage_daily
            ORDER BY trade_date;
        """)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
    conn.close()

    df = pd.DataFrame(rows, columns=cols)
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

df = load_data()

if df.empty:
    st.warning("No data found in 'alpha_vantage_daily'.")
    st.stop()

# --- User selection ---
metric = st.selectbox(
    "Select the metric to visualize:",
    ["open", "high", "low", "close", "volume"],
    index=3,  # default: close
)

# --- Create chart ---
chart = (
    alt.Chart(df)
    .mark_line(color="#4c78a8")
    .encode(
        x=alt.X("trade_date:T", title="Date"),
        y=alt.Y(f"{metric}:Q", title=f"{metric.capitalize()}"),
        tooltip=[
            alt.Tooltip("trade_date:T", title="Date"),
            alt.Tooltip(f"{metric}:Q", title=metric.capitalize(), format=",.2f"),
        ],
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

#----

st.subheader("📰 Bitcoin News")

# Load data
def load_news():
    conn = psycopg.connect(st.secrets["DBCONN"])
    cur = conn.cursor()
    cur.execute("""
        SELECT title, author, link, published_date
        FROM btc_data_news
        ORDER BY published_date DESC;
    """)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    return pd.DataFrame(rows, columns=cols)

df = load_news()

if df.empty:
    st.info("No news data available.")
else:
    df["published_date"] = pd.to_datetime(df["published_date"]).dt.date
    
    min_date = df["published_date"].min()
    max_date = df["published_date"].max()
    
    # Calendar selector
    sel_date = st.date_input("Select a date", value=max_date, min_value=min_date, max_value=max_date)
    
    filtered = df[df["published_date"] == sel_date]
    
    if filtered.empty:
        st.warning("No articles found for this date.")
    else:
        for _, row in filtered.iterrows():
            st.markdown(f"**{row['title']}**")
            st.write(f"Author: {row['author']}")
            st.markdown(f"[Read article]({row['link']})")
            st.divider()

st.write("") 
st.write("") 

st.subheader("🤖 AI Assistant")

# Configure Gemini with your key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Create the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(text)

# User input
user_input = st.chat_input("Ask something about Bitcoin...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(("user", user_input))

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_input)
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Error: {e}"
            st.markdown(reply)

    st.session_state.messages.append(("assistant", reply))
