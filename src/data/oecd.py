import pandas as pd
import requests
import io
import os

def download_oecd_dataset(dataset_id, subject_code=None):
    base_url = "https://stats.oecd.org/sdmx-json/data"
    
    if subject_code:
        url = f"{base_url}/{dataset_id}/{subject_code}/all/all"
    else:
        url = f"{base_url}/{dataset_id}/all/all/all"
    
    headers = {
        "Accept": "text/csv"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = pd.read_csv(io.StringIO(response.text))
        return data
    else:
        print(f"Error downloading {dataset_id}: {response.status_code}")
        return None

income_inequality = download_oecd_dataset("IDD", "INEQUALITY")

education_spending = download_oecd_dataset("EDU_DEM", "SPENDING")

health_spending = download_oecd_dataset("HEALTH_STAT", "SPENDING")

# Save datasets
os.makedirs('data/raw', exist_ok=True)

if income_inequality is not None:
    income_inequality.to_csv('data/raw/oecd_income_inequality.csv', index=False)
    print(f"OECD income inequality data downloaded with {len(income_inequality)} rows.")

if education_spending is not None:
    education_spending.to_csv('data/raw/oecd_education_spending.csv', index=False)
    print(f"OECD education spending data downloaded with {len(education_spending)} rows.")

if health_spending is not None:
    health_spending.to_csv('data/raw/oecd_health_spending.csv', index=False)
    print(f"OECD health spending data downloaded with {len(health_spending)} rows.")
