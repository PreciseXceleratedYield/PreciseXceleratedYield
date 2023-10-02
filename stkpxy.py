import pandas as pd
from datetime import datetime

# Read the original CSV file (if it exists)
try:
    df = pd.read_csv('stkpxy.csv')
except FileNotFoundError:
    # If the file doesn't exist, create an empty DataFrame
    df = pd.DataFrame()

# Read the data from the source CSV (fileHPdf.csv)
source_df = pd.read_csv('fileHPdf.csv')

# Add a timestamp column with the current timestamp (HH:MM)
timestamp = datetime.now().strftime('%H:%M')
timestamp_column_name = f'ltp_{timestamp}'

# Rename the 'ltp' column in the source data with the timestamp
source_df.rename(columns={'ltp': timestamp_column_name}, inplace=True)

# Select the columns you want to keep from the source data (including the renamed 'ltp' column)
selected_columns = ['tradingsymbol', 'source', 'key', timestamp_column_name]

# Merge the source data with the existing data (if any)
merged_df = pd.concat([df, source_df[selected_columns]], axis=0)

# Fill the timestamped "ltp" column with values from the "ltp" column in source data
merged_df[timestamp_column_name] = source_df[timestamp_column_name]

# Write the merged data to the existing CSV file (stkpxy.csv)
merged_df.to_csv('stkpxy.csv', index=False)
