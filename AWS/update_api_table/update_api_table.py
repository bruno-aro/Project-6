import os
import psycopg
from datetime import datetime

def update_db(event,context):
    row = event 

    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute(
        '''
        INSERT INTO alpha_vantage_daily (trade_date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (trade_date) DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
        ''',
        [
            datetime.strptime( row[0], "%Y-%m-%d"),
            float(row[1]),
            float(row[2]),
            float(row[3]),
            float(row[4]),
            float(row[5])
        ]
    )

    conn.commit()
    cur.close()
    conn.close()