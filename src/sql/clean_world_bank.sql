CREATE TABLE IF NOT EXISTS world_bank_clean AS
SELECT 
    country AS country_name,
    iso2c AS country_code,
    strftime('%Y', date) AS year,
    "GDP per capita (current US$)" AS gdp_per_capita,
    "GINI index" AS gini_index,
    "Government expenditure on education, total (% of GDP)" AS education_expenditure,
    "Current health expenditure (% of GDP)" AS health_expenditure,
    "Life expectancy at birth, total (years)" AS life_expectancy
FROM 
    world_bank_raw
WHERE 
    "GDP per capita (current US$)" IS NOT NULL
    OR "GINI index" IS NOT NULL;