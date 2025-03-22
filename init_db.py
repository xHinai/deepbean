import sqlite3

def init_db():
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    
    with open('app/init_db.sql') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db() 