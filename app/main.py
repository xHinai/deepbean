import os
from fastapi import FastAPI, HTTPException
from .models import CoffeeRoast, CoffeeScore
import databases
import sqlalchemy
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set!")
    DATABASE_URL = "sqlite:///./coffee_scores.db"  # Fallback for local development
    logger.info(f"Using fallback database: {DATABASE_URL}")
else:
    logger.info(f"Using DATABASE_URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'sqlite'}")

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

# Create tables if they don't exist (but don't recreate them or drop existing data)
# This modification ensures tables are only created if they don't exist
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine, checkfirst=True)  # Important: checkfirst=True prevents recreating existing tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    logger.info("Connecting to database...")
    await database.connect()
    logger.info("Database connection established")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnecting from database...")
    await database.disconnect()
    logger.info("Database disconnected")

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        query = "SELECT 1"
        result = await database.fetch_one(query)
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/roasts/")
async def create_roast(roast: CoffeeRoast):
    roast_dict = roast.dict()
    roast_dict['roast_id'] = str(uuid.uuid4())
    
    query = coffee_roasts.insert().values(**roast_dict)
    await database.execute(query)
    return {"roast_id": roast_dict['roast_id']}

@app.get("/roasts/")
async def get_roasts():
    query = coffee_roasts.select()
    return await database.fetch_all(query)

@app.post("/scores/")
async def create_score(score: CoffeeScore):
    score_dict = score.dict()
    score_dict['score_id'] = str(uuid.uuid4())
    
    query = coffee_scores.insert().values(**score_dict)
    await database.execute(query)
    return {"score_id": score_dict['score_id']}

@app.get("/scores/")
async def get_scores():
    query = coffee_scores.select()
    return await database.fetch_all(query) 