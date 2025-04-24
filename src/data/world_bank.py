import wbdata
import pandas as pd
from datetime import datetime

# World Bank indicator codes
indicators = {
    'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
    'SI.POV.GINI': 'GINI index',
    'SE.XPD.TOTL.GD.ZS': 'Gov expenditure on education (% of GDP)',
    'SH.XPD.CHEX.GD.ZS': 'Health expenditure (% of GDP)',
    'SP.DYN.LE00.IN': 'Life expectancy at birth (years)'
}

# Define date range
data_dates = (datetime(2000, 1, 1), datetime.today())


df = wbdata.get_dataframe(indicators=indicators, date=data_dates)
df = df.reset_index()

# Save to CSV
df.to_csv("data/raw/world_bank_data.csv", index=False)
print(f"World Bank data downloaded successfully with {len(df)} rows.")
