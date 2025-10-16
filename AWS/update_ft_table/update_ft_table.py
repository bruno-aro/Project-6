import os
import psycopg
from datetime import datetime

def update_db(event,context):
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    # Extract data from list
    title = event[0]
    link = event[1]
    author = event[2]
    date_str = event[3]

    # Convert string to datetime object
    published_date = datetime.strptime(date_str, "%b %d, %Y - %H:%M").date()

    # Generate new ID
    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM btc_data_news;")
    new_id = cur.fetchone()[0]

    # Insert data with ID
    cur.execute(
        """
        INSERT INTO btc_data_news (id, title, author, link, published_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (new_id, title, author, link, published_date)
    )

    conn.commit()
    cur.close()
    conn.close()