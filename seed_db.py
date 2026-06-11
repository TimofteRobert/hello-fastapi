from database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute(
    "INSERT INTO notes(title, content) VALUES (%s, %s)",
    ("Learn FastAPI", "Build real backend with database")
)

conn.commit()
conn.close()

print("Data inserted")