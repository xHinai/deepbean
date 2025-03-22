from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import sqlite3
import uuid

app = FastAPI()

@app.post("/roasts/")
async def create_roast(roast: CoffeeRoast):
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    roast_dict = roast.dict()
    roast_dict['roast_id'] = str(uuid.uuid4())
    
    cursor.execute("""
        INSERT INTO coffee_roasts 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(roast_dict.values()))
    conn.commit()
    return {"roast_id": roast_dict['roast_id']}

@app.get("/roasts/")
async def get_roasts():
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    roasts = cursor.execute("SELECT * FROM coffee_roasts").fetchall()
    return roasts

@app.get("/roasts/{roast_id}")
async def get_roast(roast_id: str):
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    roast = cursor.execute(
        "SELECT * FROM coffee_roasts WHERE roast_id = ?", 
        (roast_id,)
    ).fetchone()
    return roast 

@app.post("/scores/")
async def create_score(score: CoffeeScore):
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO coffee_scores (
            score_id, roast_id, date, fragrance_aroma, flavor, 
            aftertaste, acidity, body, uniformity, clean_cup, 
            sweetness, overall, defects, total_score, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        score.score_id, score.roast_id, score.date, 
        score.fragrance_aroma, score.flavor, score.aftertaste, 
        score.acidity, score.body, score.uniformity, 
        score.clean_cup, score.sweetness, score.overall, 
        score.defects, score.total_score, score.notes
    ))
    
    conn.commit()
    conn.close()
    return {"message": "Score saved successfully"}

@app.get("/scores/")
async def get_scores():
    conn = sqlite3.connect("coffee_scores.db")
    cursor = conn.cursor()
    scores = cursor.execute("SELECT * FROM coffee_scores").fetchall()
    conn.close()
    return scores 