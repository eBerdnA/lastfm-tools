import os
from datetime import datetime
from dotenv import load_dotenv

import requests
import json
import time

load_dotenv()

# Constants
API_KEY = os.getenv("API_KEY")
API_USER = os.getenv("API_USER")
API_URL = os.getenv("API_URL")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

# Function to get the Unix timestamp of the start and end of a specific year
def get_year_timestamps(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    return int(start_date.timestamp()), int(end_date.timestamp() - 1)  # End timestamp is just before the new year

# Timestamps for the start and end of 2023
start_ts, end_ts = get_year_timestamps(2023)

def get_scrobbles(api_key, user, limit=200, page=1, from_ts=None, to_ts=None):
    params = {
        'method': 'user.getrecenttracks',
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'limit': limit,
        'page': page
    }
    if from_ts:
        params['from'] = from_ts
    if to_ts:
        params['to'] = to_ts
    response = requests.get(API_URL, params=params)
    return response.json()

def download_all_scrobbles(api_key, user, from_ts, to_ts):
    current_page = 1
    total_pages = float('inf')
    all_scrobbles = []

    while current_page <= total_pages:
        response = get_scrobbles(api_key, user, page=current_page, from_ts=from_ts, to_ts=to_ts)
        if response.get('recenttracks') and response['recenttracks'].get('@attr'):
            total_pages = int(response['recenttracks']['@attr']['totalPages'])
            all_scrobbles.extend(response['recenttracks']['track'])
            print(f'Downloading page {current_page} of {total_pages}')
            current_page += 1
            time.sleep(0.2)  # Be nice to the server, avoid hitting rate limit
        else:
            break  # Stop if we don't get a proper response

    return all_scrobbles

if __name__ == "__main__":
    scrobbles = download_all_scrobbles(API_KEY, API_USER, start_ts, end_ts)
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(scrobbles, outfile)

    print(f'Download complete. Total scrobbles downloaded: {len(scrobbles)}')
