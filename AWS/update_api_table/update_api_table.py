import os
import psycopg
import datetime as dt

def update_db(event, context):
    data = event
    
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    # convert to date datatype in second function to avoid json type limitations between functions
    data[0] = dt.datetime.fromtimestamp(data[0])

    cur.execute(
        '''
            INSERT INTO weather_data(date, city, temp, feels, description)
            VALUES (%s, %s, %s, %s, %s);
        ''', 
        data
    )

    conn.commit()
    cur.close()
    conn.close()
