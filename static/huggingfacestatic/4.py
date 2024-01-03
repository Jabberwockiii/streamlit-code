import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def read_json_files(start_date, end_date):
    delta = timedelta(days=1)
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        filename = f"huggingface_models_{current_date.strftime('%Y-%m-%d')}.json"
        if os.path.exists(filename):
            df = pd.read_json(filename, lines=True)
            df['date'] = current_date
            all_data.append(df)
        current_date += delta

    return pd.concat(all_data)

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_data(df):
    # You may need to adjust these dimensions to your specific case
    plt.figure(figsize=(20, 10))

    # Generate a color map or list of line styles if you have many lines
    color_map = plt.cm.get_cmap('hsv', df['modelId'].nunique())

    for idx, model_id in enumerate(df['modelId'].unique()):
        model_data = df[df['modelId'] == model_id]
        plt.plot(model_data['date'], model_data['downloads'], label=model_id,
                 color=color_map(idx), linestyle='-', marker='o', alpha=0.7)

    plt.xlabel('Date')
    plt.ylabel('Downloads')
    plt.title('Hugging Face Model Downloads Over Time')
    
    # Place the legend outside the plot to avoid covering the lines
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the figure to a file with a tight layout to include the legend
    plt.savefig('downloads_over_time.png', bbox_inches='tight')

    # Optionally, close the plot to free up memory
    plt.close()

# Define your start and end dates for the range of files
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 2) # Adjust as needed

# Read the JSON files and merge the data
df = read_json_files(start_date, end_date)

# Plot the data
plot_data(df)

