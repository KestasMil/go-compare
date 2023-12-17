import pandas as pd
import numpy as np
import os
from datetime import datetime

primary_key = ['id']
file1, file2 = 'test_a.csv', 'test_b.csv'
separator = ','

# Create a timestamped directory name
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
results_dir = f"output/results-{timestamp}"
os.makedirs(results_dir, exist_ok=True)

# Function to load CSV only if it exists
def load_csv(filename, primary_key):
    if os.path.exists(filename):
        return pd.read_csv(filename, index_col=primary_key, sep=separator)
    else:
        print(f"File '{filename}' does not exist.")
        exit()

# Load the CSV files
df1, df2 = load_csv(f"input/{file1}", primary_key), load_csv(f"input/{file2}", primary_key)

# Convert NaN values to a string
df1 = df1.fillna('NaN')
df2 = df2.fillna('NaN')

# Finding and saving column differences if they exist
missing_cols = {
    f'Missing in {file1}': df2.columns.difference(df1.columns),
    f'Missing in {file2}': df1.columns.difference(df2.columns)
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
    # Convert MultiIndex to list of tuples
    missing_records = {k: [tuple(index) for index in v.tolist()] for k, v in missing_records.items()}
    
    # Create DataFrame from this modified dictionary
    missing_records_df = pd.DataFrame.from_dict(missing_records, orient='index').transpose()
    missing_records_df.to_csv(os.path.join(results_dir, f'missing_records_{timestamp}.csv'), index=False)

# Align indices
df1, df2 = df1.align(df2, join='outer', axis=0)

# Finding differences for matching records and saving to separate CSV files
diff = df1.compare(df2)
if not diff.empty:
    for column in diff.columns.get_level_values(0).unique():
        diff_column = diff[column].dropna().reset_index()
        #diff_column.columns = [primary_key, f'{file1} Value', f'{file2} Value']
        diff_column.columns = primary_key + [f'{file1} Value', f'{file2} Value']
        
        if not diff_column.empty:
            diff_column.to_csv(os.path.join(results_dir, f'{column}_differences_{timestamp}.csv'), index=False)
