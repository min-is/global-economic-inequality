import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
import os


logging.basicConfig(
    filename='logs/outlier_detection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def detect_outliers():
    try:
        
        os.makedirs('logs', exist_ok=True)
        
        data = pd.read_csv('data/final/inequality_data.csv')

        numerical_cols = ['gdp_per_capita', 'gini_index', 'education_expenditure', 
                         'health_expenditure', 'life_expectancy']
        
        numerical_cols = [col for col in numerical_cols if col in data.columns]
        
        outliers_report = []
        
        for year, year_data in data.groupby('year'):
            if len(year_data) < 20: 
                continue
                
            features = year_data[numerical_cols].copy()
            
            for col in features.columns:
                features[col] = features[col].fillna(features[col].median())
            
            #  NaN values
            if features.isnull().any().any():
                logging.warning(f"Year {year}: Skipping due to remaining NaN values")
                continue
            
            features_scaled = (features - features.mean()) / features.std()
            
            clf = IsolationForest(contamination=0.05, random_state=42)
            outlier_labels = clf.fit_predict(features_scaled)
            
            outlier_indices = np.where(outlier_labels == -1)[0]
            
            if len(outlier_indices) > 0:
                outlier_countries = year_data.iloc[outlier_indices]['country_name'].tolist()
                
                logging.info(f"Year {year}: Detected {len(outlier_indices)} outliers: {', '.join(outlier_countries)}")
                
                for idx in outlier_indices:
                    country_data = year_data.iloc[idx]
                    outliers_report.append({
                        'year': year,
                        'country_name': country_data['country_name'],
                        'country_code': country_data['country_code'],
                        'gdp_per_capita': country_data['gdp_per_capita'],
                        'gini_index': country_data['gini_index'],
                        'education_expenditure': country_data['education_expenditure'],
                        'health_expenditure': country_data['health_expenditure'],
                        'life_expectancy': country_data['life_expectancy'],
                    })
        
        # Save outliers report
        if outliers_report:
            outliers_df = pd.DataFrame(outliers_report)
            outliers_df.to_csv('data/processed/outliers_report.csv', index=False)
            logging.info(f"Saved outliers report with {len(outliers_df)} entries")
        else:
            logging.info("No outliers detected")
            
    except Exception as e:
        logging.error(f"Error in outlier detection: {str(e)}")

if __name__ == "__main__":
    detect_outliers()