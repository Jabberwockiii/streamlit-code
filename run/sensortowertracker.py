import requests
import json
import csv

# Function to make API requests
def fetch_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Function to save data to JSON and CSV
def save_data(data, json_filename, csv_filename):
    # Save to JSON
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file)

    # Save to CSV
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data[0].keys())  # headers
            for record in data:
                writer.writerow(record.values())

# API parameters
auth_token = 'ST0_kyi3PsB8_Qin7bdNEoqu8yA'
app_id = '1477376905'
base_url = 'https://api.sensortower.com/v1'
saved_dir = '../static/sensortowerstatic/'
# Daily Active Users (DAU) data
dau_params = {
    'app_ids': app_id,
    'countries': 'WW',
    'time_period': 'day',
    'start_date': '2021-09-01',
    'end_date': '2023-12-03',
    'auth_token': auth_token
}

dau_data = fetch_data(f'{base_url}/ios/usage/active_users', dau_params)
if dau_data:
    save_data(dau_data, saved_dir+'dau_data.json', saved_dir+'dau_data.csv')

# Download data
download_params = {
    # Assuming similar parameters structure for download data
    'app_ids': app_id,
    'countries': 'WW',
    'time_period': 'day',
    'start_date': '2021-09-01',
    'end_date': '2023-12-03',
    'auth_token': auth_token
}

download_data = fetch_data(f'{base_url}/ios/sales_report_estimates', download_params)  # Adjust endpoint as necessary

print(download_data)
if download_data:
    save_data(download_data, saved_dir+'download_data.json', saved_dir+'download_data.csv')
