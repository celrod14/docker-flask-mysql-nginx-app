from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "mydb")
    )

# Wait for DB to be ready (important in Docker!)
def wait_for_db():
    while True:
        try:
            conn = get_db_connection()
            conn.close()
            break
        except:
            print("Waiting for DB...")
            time.sleep(2)

wait_for_db()

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT
        )
    """)

    # Initialize row if empty
    cursor.execute("SELECT COUNT(*) FROM visits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO visits (count) VALUES (0)")
        conn.commit()

    # Increment counter
    cursor.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
    conn.commit()

    cursor.execute("SELECT count FROM visits WHERE id = 1")
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return f"Hello! This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)