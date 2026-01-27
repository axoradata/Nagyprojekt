import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    dbname = "elephant",
    user = "postgres",
    password = "1234567",
    port = 5432
)
cur = conn.cursor()

try:

    cur.execute("""CREATE TABLE IF NOT EXISTS employee (
            card_id VARCHAR(32) PRIMARY KEY,
            disposition VARCHAR(16) NOT NULL,
            full_name TEXT NOT NULL,
            first_day DATE NOT NULL
            );"""
    )

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
            card_id VARCHAR(32) PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            password TEXT NOT NULL,
            group_name VARCHAR(64),
            token VARCHAR(64),
            token_create_time TIMESTAMP
            );"""
    )

    cur.execute("""CREATE TABLE IF NOT EXISTS working_hours (
            card_id VARCHAR(32) PRIMARY KEY,
            check_time TIMESTAMP
            );"""
    )

    conn.commit()
    print("Table created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cur.close()
    conn.close()