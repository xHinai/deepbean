import os
from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import databases
import sqlalchemy

# Use PostgreSQL URL from environment variable or default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./coffee_scores.db")

# If using PostgreSQL, handle the URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create database connection
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define tables
coffee_roasts = sqlalchemy.Table(
    "coffee_roasts",
    metadata,
    sqlalchemy.Column("roast_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("coffee_name", sqlalchemy.String),
    sqlalchemy.Column("agtron_whole", sqlalchemy.Integer),
    sqlalchemy.Column("agtron_ground", sqlalchemy.Integer),
    sqlalchemy.Column("drop_temp", sqlalchemy.Float),
    sqlalchemy.Column("development_time", sqlalchemy.Float),
    sqlalchemy.Column("total_time", sqlalchemy.Float),
    sqlalchemy.Column("dtr_ratio", sqlalchemy.Float),
    sqlalchemy.Column("notes", sqlalchemy.String),
)

coffee_scores = sqlalchemy.Table(
    "coffee_scores",
    metadata,
    sqlalchemy.Column("score_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("roast_id", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("fragrance_aroma", sqlalchemy.Float),
    sqlalchemy.Column("flavor", sqlalchemy.Float),
    sqlalchemy.Column("aftertaste", sqlalchemy.Float),
    sqlalchemy.Column("acidity", sqlalchemy.Float),
    sqlalchemy.Column("body", sqlalchemy.Float),
    sqlalchemy.Column("uniformity", sqlalchemy.Float),
    sqlalchemy.Column("clean_cup", sqlalchemy.Float),
    sqlalchemy.Column("sweetness", sqlalchemy.Float),
    sqlalchemy.Column("overall", sqlalchemy.Float),
    sqlalchemy.Column("defects", sqlalchemy.Integer),
    sqlalchemy.Column("total_score", sqlalchemy.Float),
    sqlalchemy.Column("notes", sqlalchemy.String),
)

# Create the engine
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)  # Create tables if they don't exist

app = FastAPI()

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