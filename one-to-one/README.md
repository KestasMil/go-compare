#### This script is designed to compare two CSV files and identify differences between them. 

###### It checks for missing columns, missing records, and value discrepancies in matching records. The results of the comparison are saved in separate CSV files for easy review.

#### How to Use

##### Prepare Your Files:

Place the two CSV files you want to compare into a folder named input. Ensure that these files have a primary key column(s).

##### Configure the script:

Open one-to-one/app.py and configure the following:
primary_key = [PRIMARY KEY COLUMN NAME(S)]
file1, file2 = 'FIRST FILE NAME.csv', 'SECOND FILE NAME.csv'
separator = ',' *set csv seperator character*

##### Run the script:

Execute the script one-to-one/app.py.

##### View the Results:

After running the script, check the output folder. Inside, you will find a new folder named results-[timestamp], where [timestamp] is the date and time of the script execution.
Inside this folder, you will find the following CSV files (if applicable):
missing_columns_[timestamp].csv: Lists columns that are present in one file but missing in the other.
missing_records_[timestamp].csv: Lists records (rows) that are present in one file but missing in the other.
[column_name]_differences_[timestamp].csv: Details the differences in values for each column that is present in both files.
