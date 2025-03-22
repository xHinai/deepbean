import os
from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import databases
import sqlalchemy
import uuid

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
    sqlalchemy.Column("defects", sqlalchemy.String),
    sqlalchemy.Column("total_score", sqlalchemy.Float),
    sqlalchemy.Column("notes", sqlalchemy.String),
)

# Create the engine
engine = sqlalchemy.create_engine(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create tables
    metadata.create_all(engine)
    # Connect to the database
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/roasts/")
async def create_roast(roast: CoffeeRoast):
    query = coffee_roasts.insert().values(**roast.dict())
    await database.execute(query)
    return {"message": "Roast saved successfully"}

@app.get("/roasts/")
async def get_roasts():
    query = coffee_roasts.select()
    return await database.fetch_all(query)

@app.get("/roasts/{roast_id}")
async def get_roast(roast_id: str):
    query = coffee_roasts.select().where(coffee_roasts.c.roast_id == roast_id)
    roast = await database.fetch_one(query)
    if roast:
        return roast
    else:
        raise HTTPException(status_code=404, detail="Roast not found")

@app.post("/scores/")
async def create_score(score: CoffeeScore):
    query = coffee_scores.insert().values(**score.dict())
    await database.execute(query)
    return {"message": "Score saved successfully"}

@app.get("/scores/")
async def get_scores():
    query = coffee_scores.select()
    return await database.fetch_all(query) 