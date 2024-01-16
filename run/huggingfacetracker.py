import requests
import os
import pandas as pd
from datetime import datetime
import json

API_URL = "https://huggingface.co/api/models"
API_TOKEN = "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"

def get_models(limit=40):
    """
    Fetch the most downloaded models from Hugging Face.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    params = {
        "limit": limit,
        "config": "True",
        "direction": "-1",
        "sort": "downloads",
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def main():
    try:
        models = get_models()
        df = pd.DataFrame(models)

        if 'downloads' in df.columns and 'modelId' in df.columns and 'likes' in df.columns:
            df = df[['modelId', 'downloads', 'likes']]
        else:
            raise Exception("Required fields are missing in the data")

        today = datetime.now().strftime('%Y-%m-%d')
        excel_filename = f"/home/ubuntu/streamlit-code/static/huggingfacestatic/huggingface_models_{today}.xlsx"
        json_filename = f"/home/ubuntu/streamlit-code/static/huggingfacestatic/huggingface_models_{today}.json"

        # Save to Excel
        df.to_excel(excel_filename, index=False)
        print(f"Data saved to {excel_filename}")

        # Save to JSON
        df.to_json(json_filename, orient='records', lines=True)
        print(f"Data saved to {json_filename}")
        
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()

