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

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Print out which database we're using (for debugging)
if DATABASE_URL:
    logger.info(f"Using DATABASE_URL: {DATABASE_URL.split('@')[0]}...")
    # If using PostgreSQL, convert the URL format
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        logger.info("Fixed PostgreSQL URL format")
else:
    # Do NOT allow fallback to SQLite
    raise Exception("DATABASE_URL environment variable not set! Cannot proceed without a database connection.")

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

# Create engine and attempt to create tables
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    logger.info("Created database engine")
    
    # Try to create tables if they don't exist
    metadata.create_all(engine, checkfirst=True)
    logger.info("Database tables initialized")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise e  # Re-raise the exception to fail startup if database isn't available

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        logger.info("Connecting to database...")
        await database.connect()
        logger.info("Database connection established")
        
        # Verify tables exist by querying them
        query = "SELECT * FROM coffee_roasts LIMIT 1"
        result = await database.fetch_one(query)
        logger.info(f"Test query result: {result}")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise e  # Fail startup if database isn't working

@app.on_event("shutdown")
async def shutdown():
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