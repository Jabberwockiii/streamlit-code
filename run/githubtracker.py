from playwright.sync_api import sync_playwright
import re
import requests
from datetime import datetime
import pandas as pd
import os

def scrape_jetbrains_plugin():
    with sync_playwright() as p:
        # Launch a new browser instance
        browser = p.chromium.launch()

        # Create a new page
        page = browser.new_page()

        # Navigate to the JetBrains plugin URL
        page.goto("https://plugins.jetbrains.com/plugin/17718-github-copilot")

        # Wait for the content to render
        page.wait_for_selector('span[data-testid="total-votes"]')  # Updated the selector

        # Extract the ratings and downloads
        ratings = page.text_content('span[data-testid="total-votes"]')  # Updated the selector
        downloads = page.text_content('span.rs-text-3_hardness_pale')  # Updated the selector

        # Close the browser
        browser.close()

        return ratings, downloads

def scrape_vscode_marketplace():
    URL = "https://marketplace.visualstudio.com/items?itemName=GitHub.copilot"
    response = requests.get(URL)
    match = re.search(r'<span class="installs-text" title="The number of unique installations, not including updates\."> ([\d,]+) installs</span>', response.text)
    if match:
        installs = match.group(1)
    else:
        installs = "Not found"
    return installs

def write_to_excel(ratings, downloads, vscode_installs):
    timestamp = datetime.now()
    data = {
        "Timestamp": [timestamp],
        "JetBrains Ratings": [ratings],
        "JetBrains Downloads": [downloads],
        "VSCode Installs": [vscode_installs]
    }
    df = pd.DataFrame(data)

    excel_file = '../static/copilotstatic/scraped_info.xlsx'
    if os.path.exists(excel_file):
        df_existing = pd.read_excel(excel_file)
        df = pd.concat([df_existing, df], ignore_index=True)

    df.to_excel(excel_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    ratings, downloads = scrape_jetbrains_plugin()
    vscode_installs = scrape_vscode_marketplace()

    print(f"JetBrains Ratings: {ratings}")
    print(f"JetBrains Downloads: {downloads}")
    print(f"VSCode Installs: {vscode_installs}")

    write_to_excel(ratings, downloads, vscode_installs)

