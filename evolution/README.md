#### Purpose

This script is designed for tracking the evolution of data records over time in a single CSV file. It focuses on tracking changes in each record's values based on a specified primary key and a date column. The script generates detailed output files that showcase how each data point has changed.

This script is helpful for users who need to track changes in data over time, especially useful in scenarios like data auditing or historical data analysis.

#### How to Use

##### Prepare Your File

Place your CSV file into an input folder. Ensure that the file has a primary key column(s) and a column that indicates the validity date of each record.

##### Configure the Script

Open the script file (evolution/app.py) and adjust the config dictionary at the top:
- "csv_file": Set to the name of your CSV file (e.g., "tests/test1.csv").
- "primary_keys": Specify the column name(s) that uniquely identify each record (e.g., ["id"]).
- "order_by_columns": Specify the column that represents the date of validity (e.g., ["date_valid"]).
- "note": Optionally add a note that will be stored in the results folder.

##### Run the Script

Execute the script. This can typically be done by opening the script in a Python environment and running it, or by using a command in a terminal or command prompt.

##### View the Results

After running the script, navigate to the output directory.
Inside, you will find a new folder named output/[subdirectory]/[csv_file_name]/results-[timestamp], where [subdirectory] is derived from the path of your CSV file, [csv_file_name] is the name of your CSV file, and [timestamp] is the date and time of the script execution.

In this folder, you'll find CSV files for each primary key and column showing the evolution of their values. Each file is named as [primary_key]_[column_name]_[number_of_changes].csv.

Additionally, a run_info.json file will be present, containing the configuration details and timestamp of the run.

#### Note

Make sure Python and necessary libraries (pandas, numpy, os, datetime) are installed in your environment.
