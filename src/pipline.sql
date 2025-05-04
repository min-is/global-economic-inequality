-- Staging schema 
CREATE SCHEMA IF NOT EXISTS staging;

-- staging table
CREATE TABLE IF NOT EXISTS staging.economic_data (
    country_name VARCHAR(100),
    country_code CHAR(3),
    year INT,
    gini_index DECIMAL(5,2),
    gdp_per_capita DECIMAL(12,2),
    gdp_current DECIMAL(15,2),
    gdp_growth DECIMAL(5,2),
    decade INT
);

-- Load data 
COPY staging.economic_data FROM 'global_economic_data.csv' DELIMITER ',' CSV HEADER;

-- production schema 
CREATE SCHEMA IF NOT EXISTS production;

-- production table
CREATE TABLE IF NOT EXISTS production.economic_metrics (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(100),
    country_code CHAR(3),
    year INT,
    decade INT,
    gini_index DECIMAL(5,2),
    gdp_per_capita DECIMAL(12,2),
    gdp_current DECIMAL(15,2),
    gdp_growth DECIMAL(5,2),
    inequality_ratio DECIMAL(12,4) GENERATED ALWAYS AS (gini_index / NULLIF(gdp_per_capita, 0)) STORED,
    UNIQUE (country_code, year)
);

INSERT INTO production.economic_metrics (country_name, country_code, year, decade, gini_index, gdp_per_capita, gdp_current, gdp_growth)
SELECT 
    country_name,
    country_code,
    year,
    decade,
    gini_index,
    gdp_per_capita,
    gdp_current,
    gdp_growth
FROM staging.economic_data
ON CONFLICT (country_code, year) DO UPDATE SET
    country_name = EXCLUDED.country_name,
    decade = EXCLUDED.decade,
    gini_index = EXCLUDED.gini_index,
    gdp_per_capita = EXCLUDED.gdp_per_capita,
    gdp_current = EXCLUDED.gdp_current,
    gdp_growth = EXCLUDED.gdp_growth;
