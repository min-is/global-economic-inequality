import schedule
import time
import subprocess
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='logs/automated_refresh.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_data_pipeline():
    """Run the entire data pipeline and log results"""
    try:
        logging.info("Starting automated data refresh...")
        
        # Run download scripts
        subprocess.run(["python", "src/data/world_bank.py"], check=True)
        subprocess.run(["python", "src/data/un_hdi.py"], check=True)
        subprocess.run(["python", "src/data/oecd.py"], check=True)
        
        # Process data
        subprocess.run(["python", "src/sql/db.py"], check=True)
        subprocess.run(["python", "src/features/data_processing.py"], check=True)
        
        # Run analysis
        subprocess.run(["python", "src/models/inequality_metrics.py"], check=True)
        subprocess.run(["python", "src/models/regression_analysis.py"], check=True)
        
        # Create visualizations
        subprocess.run(["python", "src/visualization/choropleth_maps.py"], check=True)
        subprocess.run(["python", "src/visualization/radial_bar.py"], check=True)
        subprocess.run(["python", "src/visualization/scatter_plots.py"], check=True)
        
        # Prepare for Tableau
        subprocess.run(["python", "src/visualization/tableau.py"], check=True)
        
        # Run outlier detection
        subprocess.run(["python", "src/models/outlier_detection.py"], check=True)
        
        logging.info("Data refresh completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in data refresh: {str(e)}")

# Schedule to run monthly
schedule.every().month.at("01:00").do(run_data_pipeline)

if __name__ == "__main__":
    print("Starting automated data refresh scheduler...")
    print("Press Ctrl+C to exit")
    
    run_data_pipeline()
    
    while True:
        schedule.run_pending()
        time.sleep(60)