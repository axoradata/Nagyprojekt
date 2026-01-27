import psycopg2


def insert_into(sql_query:str):
    conn = psycopg2.connect(
    host="localhost",
    dbname="elephant",
    user="postgres",
     password="1234567",
    port=5432)
    cur = conn.cursor()

    try:
        cur.execute(sql_query)

        conn.commit()

    except Exception as e:
        print("Database error in 'insert into' branch because:")
        print(e)
    finally:
        cur.close()
        conn.close()

def select(sql_query:str):
    conn = psycopg2.connect(
    host="localhost",
    dbname="elephant",
    user="postgres",
     password="1234567",
    port=5432)
    cur = conn.cursor()

    fetch = None

    try:
        cur.execute(sql_query)

        fetch = cur.fetchone()
        conn.commit()

    except Exception as e:
        print("Database error in 'select' branch because:")
        print(e)
    finally:
        cur.close()
        conn.close()
        if fetch:
            return fetch
        else:
            return None

def select_all(sql_query:str):
    conn = psycopg2.connect(
    host="localhost",
    dbname="elephant",
    user="postgres",
     password="1234567",
    port=5432)
    cur = conn.cursor()

    fetch = None

    try:
        cur.execute(sql_query)

        fetch = cur.fetchall()
        conn.commit()

    except Exception as e:
        print("Database error in 'select' branch because:")
        print(e)
    finally:
        cur.close()
        conn.close()
        if fetch:
            return fetch
        else:
            return None