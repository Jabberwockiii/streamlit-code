import requests
import pandas as pd
from datetime import datetime
import time
import os 

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return [line.split(':') for line in lines]

repopairs = load_data('repos.txt')

owners = [pair[0] for pair in repopairs]
repositories = [pair[1] for pair in repopairs]

data = {'Repository': [], 'Stars': [], 'Watches': [], 'Forks': []}

# Add your GitHub personal access token here
token = "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"
headers = {
    'Authorization': f'token {token}'
}
counter = 1 
for owner, repo in zip(owners, repositories):
    if counter % 20 == 0: 
         time.sleep(3600)
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    
    # Handling rate limit and quotas
    try:
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}')

        if response.status_code == 200:
            repo_data = response.json()
            data['Repository'].append(owner + '/' + repo)
            data['Stars'].append(repo_data['stargazers_count'])
            data['Watches'].append(repo_data['subscribers_count'])
            data['Forks'].append(repo_data['forks_count'])
            print(f"Repo: {repo}, Stars: {repo_data['stargazers_count']}, Watches: {repo_data['subscribers_count']}, Forks: {repo_data['forks_count']}")
        elif response.status_code == 404:
            print(f"Repository {repo} not found.")
        else:
            # Handle other errors (like rate limits, server errors, etc.)
            print(f"Failed to retrieve data for {repo}. Status code: {response.status_code}, {response.json()}")
            # You can also access response.text or response.json() here to get more details about the failure if the API provides it.
        
        time.sleep(1)  # Sleep to avoid hitting rate limit
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
    time.sleep(1)  # Avoid hitting rate limit

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

filename = f"/home/ubuntu/streamlit-code/static/githubstatic/github_data.xlsx"
today = datetime.now().strftime('%Y-%m-%d')

if os.path.exists(filename):
    existing_df = pd.read_excel(filename, engine='openpyxl')
    
    # Add a column of empty strings as a separator
    separator = pd.Series(['' for _ in range(len(existing_df))], name=today)
    existing_df = pd.concat([existing_df, separator], axis=1)
    
    # Concatenate horizontally with the existing DataFrame
    final_df = pd.concat([existing_df, df], axis=1)
else:
    # If file does not exist, just use the new DataFrame
    final_df = df

# Write the final DataFrame to an Excel file
final_df.to_excel(filename, index=False, engine='openpyxl')