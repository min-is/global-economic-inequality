CREATE TABLE IF NOT EXISTS merged_inequality_data AS
SELECT 
    wb.country_name,
    wb.country_code,
    wb.year,
    wb.gdp_per_capita,
    wb.gini_index,
    wb.education_expenditure,
    wb.health_expenditure,
    wb.life_expectancy,
    hdi.hdi_value,
    hdi.hdi_rank,
    oecd_ineq.p90_p10_ratio,
    oecd_edu.edu_spend_pct_gdp,
    oecd_health.health_spend_pct_gdp
FROM 
    world_bank_clean wb
LEFT JOIN 
    (SELECT country_code, year, hdi_value, hdi_rank FROM un_hdi_clean) hdi 
    ON wb.country_code = hdi.country_code AND wb.year = hdi.year
LEFT JOIN 
    (SELECT country_code, year, p90_p10_ratio FROM oecd_inequality_clean) oecd_ineq
    ON wb.country_code = oecd_ineq.country_code AND wb.year = oecd_ineq.year
LEFT JOIN 
    (SELECT country_code, year, edu_spend_pct_gdp FROM oecd_education_clean) oecd_edu
    ON wb.country_code = oecd_edu.country_code AND wb.year = oecd_edu.year
LEFT JOIN 
    (SELECT country_code, year, health_spend_pct_gdp FROM oecd_health_clean) oecd_health
    ON wb.country_code = oecd_health.country_code AND wb.year = oecd_health.year
WHERE 
    wb.year BETWEEN 2000 AND 2024
ORDER BY 
    wb.country_name, wb.year;