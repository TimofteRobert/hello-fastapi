import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="notesdb",
    user="appuser",
    password="apppassword"
)

print("connected successfully!")

conn.close()