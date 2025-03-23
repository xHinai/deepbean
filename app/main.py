from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import sqlite3
import uuid

app = FastAPI()

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('coffee_scores.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS coffee_roasts (
            roast_id TEXT PRIMARY KEY,
            date TEXT,
            coffee_name TEXT,
            agtron_whole INTEGER,
            agtron_ground INTEGER,
            drop_temp REAL,
            development_time REAL,
            total_time REAL,
            dtr_ratio REAL,
            notes TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS coffee_scores (
            score_id TEXT PRIMARY KEY,
            roast_id TEXT,
            date TEXT,
            fragrance_aroma REAL,
            flavor REAL,
            aftertaste REAL,
            acidity REAL,
            body REAL,
            uniformity REAL,
            clean_cup REAL,
            sweetness REAL,
            overall REAL,
            defects INTEGER,
            total_score REAL,
            notes TEXT,
            FOREIGN KEY(roast_id) REFERENCES coffee_roasts(roast_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/roasts/")
def create_roast(roast: CoffeeRoast):
    conn = sqlite3.connect('coffee_scores.db')
    c = conn.cursor()
    
    roast_dict = roast.dict()
    roast_dict['roast_id'] = str(uuid.uuid4())
    
    c.execute('''
        INSERT INTO coffee_roasts 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(roast_dict.values()))
    
    conn.commit()
    conn.close()
    return {"roast_id": roast_dict['roast_id']}

@app.get("/roasts/")
def get_roasts():
    conn = sqlite3.connect('coffee_scores.db')
    c = conn.cursor()
    roasts = c.execute("SELECT * FROM coffee_roasts").fetchall()
    conn.close()
    return roasts

@app.post("/scores/")
def create_score(score: CoffeeScore):
    conn = sqlite3.connect('coffee_scores.db')
    c = conn.cursor()
    
    score_dict = score.dict()
    score_dict['score_id'] = str(uuid.uuid4())
    
    c.execute('''
        INSERT INTO coffee_scores 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(score_dict.values()))
    
    conn.commit()
    conn.close()
    return {"score_id": score_dict['score_id']}

@app.get("/scores/")
def get_scores():
    conn = sqlite3.connect('coffee_scores.db')
    c = conn.cursor()
    scores = c.execute("SELECT * FROM coffee_scores").fetchall()
    conn.close()
    return scores 