import opendatasets as od
import os
import pandas as pd

un_hdi_url = "https://www.kaggle.com/datasets/undp/human-development"
od.download(un_hdi_url, data_dir='data/raw')

hdi_dir = os.path.join('data/raw', 'human-development')
hdi_file = os.path.join(hdi_dir, 'human_development.csv')  

if os.path.exists(hdi_file):
    hdi_data = pd.read_csv(hdi_file)
    

    hdi_data.to_csv('data/raw/un_hdi_data.csv', index=False)
    print(f"UN HDI data processed successfully with {len(hdi_data)} rows.")
else:
    print(f"Error: Could not find the expected HDI file at {hdi_file}")