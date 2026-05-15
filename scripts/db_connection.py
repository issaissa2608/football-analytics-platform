import psycopg2

try:
    conn = psycopg2.connect(
        dbname="football_analytics",
        user="postgres",
        password="Postgres",
        host="localhost",
        port="5433"
    )

    print("✅ Connection successful")

    cur = conn.cursor()
    cur.execute("SELECT version();")

    db_version = cur.fetchone()
    print("PostgreSQL version:", db_version)

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed")
    print(e)