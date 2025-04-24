import sqlite3
import pandas as pd
import os

def create_database():
    """Create SQLite database and load raw data"""
    conn = sqlite3.connect('data/processed/inequality_database.db')
    
    # Load raw data
    world_bank = pd.read_csv('data/raw/world_bank_data.csv')
    un_hdi = pd.read_csv('data/raw/un_hdi_data.csv')
    oecd_inequality = pd.read_csv('data/raw/oecd_income_inequality.csv')
    oecd_education = pd.read_csv('data/raw/oecd_education_spending.csv')
    oecd_health = pd.read_csv('data/raw/oecd_health_spending.csv')
    
    world_bank.to_sql('world_bank_raw', conn, if_exists='replace', index=False)
    un_hdi.to_sql('un_hdi_raw', conn, if_exists='replace', index=False)
    oecd_inequality.to_sql('oecd_inequality_raw', conn, if_exists='replace', index=False)
    oecd_education.to_sql('oecd_education_raw', conn, if_exists='replace', index=False)
    oecd_health.to_sql('oecd_health_raw', conn, if_exists='replace', index=False)
    
    # Create continent and economic bloc reference tables 
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()