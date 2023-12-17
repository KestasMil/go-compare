import pandas as pd
import os
import json
from datetime import datetime
import numpy as np

# CONFIG for this run
config = {
    "csv_file": "tests/test1.csv",
    "primary_keys": ["id"],
    "order_by_columns": ["date_valid"],
    "note": ""  # Note is stored within results folder for each run.
}

# Init globals
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
debug_grouping_and_ordering = False
debug_cell_iterator = False

# Construct the output folder path
base_filename = os.path.basename(config["csv_file"])
output_root_dir = f"output/{os.path.dirname(config['csv_file'])}/{base_filename}/results_{timestamp}"

# Create output folder
os.makedirs(output_root_dir, exist_ok=True)

def log_run_info():
    config["run_timestamp"] = timestamp
    json_file_path = os.path.join(output_root_dir, "run_info.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(config, json_file, indent=4)

def track_changes():
    df = pd.read_csv(os.path.join("input", config["csv_file"]))
    df.sort_values(by=config["order_by_columns"], inplace=True)

    results = []

    for key, group_df in df.groupby(config["primary_keys"]):
        # Handle both single and multiple primary keys
        if not isinstance(key, tuple):
            key = (key,)  # Make it a tuple for consistency
        
        record_count = len(group_df)  # Count of records for the current key
        current_rec = {}

        for index, row in group_df.iterrows():
            valid_from = tuple(row[col] for col in config["order_by_columns"])

            for col_name, cell_value in row.items():
                if pd.isna(cell_value):  # Check if the cell value is NaN
                    cell_value = None  # Convert NaN to None

                # Initialize the current_rec for this column if not already done
                if col_name not in current_rec:
                    current_rec[col_name] = {'col_name': col_name, 'key': key, 'valid_from': valid_from, 'value': cell_value, 'value_valid_for': 0}

                # Compare current value with previous one, treating None values as equal
                if (current_rec[col_name]['value'] != cell_value) and not (current_rec[col_name]['value'] is None and cell_value is None):
                    results.append(current_rec[col_name])
                    current_rec[col_name] = {'col_name': col_name, 'key': key, 'valid_from': valid_from, 'value': cell_value, 'value_valid_for': 1}
                else:
                    current_rec[col_name]['value_valid_for'] += 1

                if index == group_df.index[-1]:
                    results.append(current_rec[col_name])

    # Write results to CSV
    for key, group in pd.DataFrame(results).groupby(['key', 'col_name']):
        key_str = '_'.join(map(str, key[0]))  # Convert the primary key to a string
        col_name = key[1]
        group = group[['key', 'valid_from', 'value', 'value_valid_for']]  # Reorder columns

        # Correct way to filter and count records for the current key
        key_filter = True
        for i, col in enumerate(config["primary_keys"]):
            key_filter &= (df[col] == key[0][i])
        
        record_count = df[key_filter].shape[0]
        folder_name = f"{key_str}_(count-{record_count})"
        
        filename = f"{col_name}_{len(group)}.csv"
        filepath = os.path.join(output_root_dir, folder_name, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        group.to_csv(filepath, index=False)


log_run_info()
track_changes()