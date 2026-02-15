import psycopg2
from log import get_time

def data_formating(data:str) -> str:
    formed_data = data.replace('TAG:', '')
    return formed_data[0:19]

def db_data_in(card_id):
    conn = psycopg2.connect(
        host="localhost",
        dbname="elephant",
        user="postgres",
        password="1234567",
        port=5432
    )
    cur = conn.cursor()

    try:
        data = data_formating(card_id)
        print("DB>>" + data)

        cur.execute(f"""
                        SELECT full_name FROM employee WHERE card_id = '{data}';
                    """)
        response = cur.fetchone()
        conn.commit()

        #print("Teszteles>> " + response)

        if response is not None:
            return str(response)
        else:
            return 0
    except Exception as e:
        print("Adat hiba //data_is_init// function", e)
        return 0
    finally:
        cur.close()
        conn.close()

def db_write_log(card_id):
    conn = psycopg2.connect(
        host="localhost",
        dbname="elephant",
        user="postgres",
        password="1234567",
        port=5432
    )
    cur = conn.cursor()

    try:
        data = data_formating(card_id)
        time = get_time()
        print("DB>>" + data)

        cur.execute(f"""
                        INSERT INTO working_hours (card_id, check_time) VALUES ('{data}', '{time}');
                    """)
        conn.commit()

    except Exception as e:
        print("Adat hiba //data_write_log// function", e)
        return 0
    finally:
        cur.close()
        conn.close()