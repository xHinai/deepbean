import os
from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import databases
import sqlalchemy
import uuid

# Use PostgreSQL URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

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

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health")
async def health_check():
    try:
        query = "SELECT 1"
        await database.execute(query)
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/roasts/")
async def create_roast(roast: CoffeeRoast):
    query = coffee_roasts.insert().values(
        roast_id=str(uuid.uuid4()),
        date=roast.date,
        coffee_name=roast.coffee_name,
        agtron_whole=roast.agtron_whole,
        agtron_ground=roast.agtron_ground,
        drop_temp=roast.drop_temp,
        development_time=roast.development_time,
        total_time=roast.total_time,
        dtr_ratio=roast.dtr_ratio,
        notes=roast.notes
    )
    await database.execute(query)
    return {"message": "Roast created successfully"}

@app.get("/roasts/")
async def get_roasts():
    query = coffee_roasts.select()
    return await database.fetch_all(query)

@app.post("/scores/")
async def create_score(score: CoffeeScore):
    query = coffee_scores.insert().values(
        score_id=str(uuid.uuid4()),
        roast_id=score.roast_id,
        date=score.date,
        fragrance_aroma=score.fragrance_aroma,
        flavor=score.flavor,
        aftertaste=score.aftertaste,
        acidity=score.acidity,
        body=score.body,
        uniformity=score.uniformity,
        clean_cup=score.clean_cup,
        sweetness=score.sweetness,
        overall=score.overall,
        defects=score.defects,
        total_score=score.total_score,
        notes=score.notes
    )
    await database.execute(query)
    return {"message": "Score created successfully"}

@app.get("/scores/")
async def get_scores():
    query = coffee_scores.select()
    return await database.fetch_all(query) 