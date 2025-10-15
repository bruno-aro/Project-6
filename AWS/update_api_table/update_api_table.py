import os
import psycopg
import datetime as dt 

def update_db(event, context):
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS btc_data_news(
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            link TEXT,
            published_date DATE
        );
    ''')

    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM btc_data_news;")
    next_id = cur.fetchone()[0]

    cur.execute(
        '''
        INSERT INTO btc_data_news (id, title, author, link, published_date)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        ''',
        [
            next_id,
            event.get("title", ""),
            event.get("author", ""),
            event.get("link", ""),
            dt.datetime.now(dt.timezone.utc).date()
        ]
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"statusCode": 200, "id": next_id}