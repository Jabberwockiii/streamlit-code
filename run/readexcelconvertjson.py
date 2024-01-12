import pandas as pd
import json
from datetime import datetime
import re
# use regex to extract column names 
def clean_column_name(col):
    col = re.sub(r'\.\d+', '', col)  # Remove .number
    return col
def create_json_files(file_path):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Calculate the number of groups (each group contains 5 columns)
    num_groups = len(data.columns) // 5
    # Process each group
    for i in range(num_groups):
        # Select columns for the current group
        group_data = data.iloc[:, i*5:(i+1)*5]
        # use the last column first row as the date separator
        date = group_data.columns[-1].split('.')[0]
        # save the first 4 columns in json
        # clean the column names 
        group_data.columns = [clean_column_name(col) for col in group_data.columns]
        print(group_data.columns)
        group_data.to_json(f"./githubstatic/github_data_{date}.json", orient='records', lines=True) 
# Example usage
create_json_files('./githubstatic/github_data.xlsx')
