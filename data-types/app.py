from decimal import Decimal
import pandas as pd

input_file = "test.csv"
default_type = "N/A"
output_format_template = "[{col_name}] -> {data_type}"
# Adjust threshold for Decimal type inference
precision_threshold = 4

def read_csv_to_df(file_name: str) -> pd.DataFrame:
    file_path = f"input/{file_name}"
    df = pd.read_csv(file_path)
    return df

def try_parse_datetime(df, col_name):
    """Attempt to parse a column as datetime, handling exceptions."""
    try:
        if df[col_name].dtype == 'object':
            temp_series = pd.to_datetime(df[col_name], errors='coerce')
            # Check if all non-NaN entries in the original series were successfully parsed
            if temp_series.notna().equals(df[col_name].notna()):
                return temp_series
    except AttributeError as e:
        print(f"Error parsing column '{col_name}' as datetime: {e}")
    return df[col_name]

def is_boolean(series):
    # Define potential boolean values
    boolean_values = {'True', 'False', 'true', 'false', '1', '0', 'YES', 'NO', 'Yes', 'No', 'T', 'F', 'yes', 'no', 't', 'f', 0, 1}
    return all(item in boolean_values or pd.isna(item) for item in series)

def infer_spark_data_types(df) -> dict:
    def map_type(pandas_dtype, series):
        if pd.isna(series).all():
            return default_type
        elif is_boolean(series):
            return "BooleanType"
        elif pd.api.types.is_integer_dtype(series.dropna()):
            if series.max() <= 2147483647 and series.min() >= -2147483648:  # 32-bit integer range
                return "IntegerType"
            else:
                return "LongType"
        elif pd.api.types.is_float_dtype(pandas_dtype):
            # Check if the float values can be converted to integers
            if all(series.dropna().apply(lambda x: x.is_integer())):
                return "IntegerType" if series.max() <= 2147483647 and series.min() >= -2147483648 else "LongType"
            if any(isinstance(x, Decimal) for x in series.dropna()) or is_high_precision(series):
                return "DecimalType"
            return "FloatType"
        elif pd.api.types.is_string_dtype(pandas_dtype):
            return "StringType"
        elif pd.api.types.is_bool_dtype(pandas_dtype):
            return "BooleanType"
        elif pd.api.types.is_datetime64_any_dtype(pandas_dtype):
            if series.dropna().dt.time.apply(lambda t: t.hour == 0 and t.minute == 0 and t.second == 0 and t.microsecond == 0).all():
                return "DateType"
            else:
                return "TimestampType"
        else:
            return "StringType"
        
    def is_high_precision(series):
        return series.dropna().apply(lambda x: isinstance(x, float) and len(str(x).split('.')[-1]) > precision_threshold).any()

    # Check for potential datetime columns
    for col in df.columns:
        df[col] = try_parse_datetime(df, col)

    type_dict = {}
    for col in df.columns:
        type_dict[col] = map_type(df[col].dtype, df[col])

    return type_dict

def write_output(file_name: str, data: dict):
    output_path = f"output/{file_name.split('.')[0]}.txt"
    with open(output_path, 'w') as file:
        for col_name, data_type in data.items():
            formatted_line = output_format_template.format(col_name=col_name, data_type=data_type)
            file.write(formatted_line + '\n')

# Usage:
df = read_csv_to_df(input_file)
data_types = infer_spark_data_types(df)
write_output(input_file, data_types)
