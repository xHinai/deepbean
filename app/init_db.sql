CREATE TABLE coffee_roasts (
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
);

CREATE TABLE coffee_scores (
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
); 