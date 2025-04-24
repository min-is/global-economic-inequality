import sqlite3
import pandas as pd
import os

def execute_sql_script(conn, script_path):
    """Execute a SQL script file"""
    with open(script_path, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()

def process_data():
    conn = sqlite3.connect('data/processed/inequality_database.db')
    sql_dir = 'src/sql'
    execute_sql_script(conn, os.path.join(sql_dir, 'clean_world_bank.sql'))
    execute_sql_script(conn, os.path.join(sql_dir, 'clean_un_hdi.sql'))
    execute_sql_script(conn, os.path.join(sql_dir, 'clean_oecd_inequality.sql'))
    execute_sql_script(conn, os.path.join(sql_dir, 'clean_oecd_education.sql'))
    execute_sql_script(conn, os.path.join(sql_dir, 'clean_oecd_health.sql'))
    execute_sql_script(conn, os.path.join(sql_dir, 'merge_datasets.sql'))
    
    # Export final merged dataset
    merged_data = pd.read_sql("SELECT * FROM merged_inequality_data", conn)
    merged_data.to_csv('data/final/inequality_data.csv', index=False)
    
    conn.close()
    print(f"Data processing complete. Final dataset has {len(merged_data)} rows.")

if __name__ == "__main__":
    process_data()