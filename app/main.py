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

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set! Cannot proceed without a database connection.")

# If using PostgreSQL, convert the URL format
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

green_beans = sqlalchemy.Table(
    "green_beans",
    metadata,
    sqlalchemy.Column("bean_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("origin", sqlalchemy.String),
    sqlalchemy.Column("processing", sqlalchemy.String),
    sqlalchemy.Column("variety", sqlalchemy.String),
    sqlalchemy.Column("altitude", sqlalchemy.String),
    sqlalchemy.Column("purchase_date", sqlalchemy.String),
    sqlalchemy.Column("initial_stock_kg", sqlalchemy.Float),
    sqlalchemy.Column("current_stock_kg", sqlalchemy.Float),
    sqlalchemy.Column("price_per_kg", sqlalchemy.Float),
    sqlalchemy.Column("supplier", sqlalchemy.String),
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
    raise e

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        logger.info("Connecting to database...")
        await database.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise e

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

@app.post("/green-beans/")
async def create_green_bean(green_bean: dict):
    bean_id = str(uuid.uuid4())
    green_bean["bean_id"] = bean_id
    
    # Set current_stock equal to initial_stock at creation
    if "initial_stock_kg" in green_bean:
        green_bean["current_stock_kg"] = green_bean["initial_stock_kg"]
    
    query = green_beans.insert().values(**green_bean)
    await database.execute(query)
    return {"bean_id": bean_id}

@app.get("/green-beans/")
async def get_green_beans():
    query = green_beans.select()
    return await database.fetch_all(query)

@app.put("/green-beans/{bean_id}/update-stock")
async def update_bean_stock(bean_id: str, amount_used: float):
    # First get current stock
    select_query = green_beans.select().where(green_beans.c.bean_id == bean_id)
    bean = await database.fetch_one(select_query)
    
    if not bean:
        raise HTTPException(status_code=404, detail="Green bean not found")
    
    # Calculate new stock and update
    current_stock = bean["current_stock_kg"]
    new_stock = max(0, current_stock - amount_used)  # Prevent negative stock
    
    update_query = green_beans.update().where(
        green_beans.c.bean_id == bean_id
    ).values(current_stock_kg=new_stock)
    
    await database.execute(update_query)
    return {"bean_id": bean_id, "new_stock_kg": new_stock} 