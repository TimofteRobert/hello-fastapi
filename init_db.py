from database import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
 """)

conn.commit()
conn.close()

print("Table created successfully")
