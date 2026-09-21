import sqlite3
from fastapi import FastAPI

app = FastAPI()
conn = sqlite3.connect("test.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0
)
""")

conn.commit()



@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API!"}