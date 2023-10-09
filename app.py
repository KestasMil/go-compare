import pandas as pd
import numpy as np
import os
from datetime import datetime

primary_key = 'id'
file1, file2 = 'a.csv', 'b.csv'
separator = ','

# Create a timestamped directory name
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
results_dir = f"results-{timestamp}"
os.makedirs(results_dir, exist_ok=True)

# Function to load CSV only if it exists
def load_csv(filename, primary_key):
    if os.path.exists(filename):
        return pd.read_csv(filename, index_col=primary_key, sep=separator)
    else:
        print(f"File '{filename}' does not exist.")
        exit()

# Load the CSV files
df1, df2 = load_csv(file1, primary_key), load_csv(file2, primary_key)

# Finding and saving column differences if they exist
missing_cols = {
    'Missing Columns in a.csv': df2.columns.difference(df1.columns),
    'Missing Columns in b.csv': df1.columns.difference(df2.columns)
}

if any(len(cols) > 0 for cols in missing_cols.values()):
    missing_cols_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in missing_cols.items()]))
    missing_cols_df.to_csv(os.path.join(results_dir, f'missing_columns_{timestamp}.csv'), index=False)

# Handle missing columns
df1, df2 = df1.align(df2, join='outer', axis=1)

# Finding and saving missing records if they exist
missing_records = {
    f'Missing in {file1}': df2.index.difference(df1.index),
    f'Missing in {file2}': df1.index.difference(df2.index)
}

if any(len(records) > 0 for records in missing_records.values()):
    missing_records_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in missing_records.items()]))
    missing_records_df.to_csv(os.path.join(results_dir, f'missing_records_{timestamp}.csv'), index=False)

# Align indices
df1, df2 = df1.align(df2, join='outer', axis=0)

# Finding differences for matching records and saving to separate CSV files
diff = df1.compare(df2)
if not diff.empty:
    for column in diff.columns.get_level_values(0).unique():
        diff_column = diff[column].dropna().reset_index()
        diff_column.columns = [primary_key, f'{file1} Value', f'{file2} Value']
        
        if not diff_column.empty:
            diff_column.to_csv(os.path.join(results_dir, f'{column}_differences_{timestamp}.csv'), index=False)
