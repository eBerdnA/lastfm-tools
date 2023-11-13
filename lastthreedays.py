# path/filename: ./scrobble_downloader.py

import requests
from datetime import datetime, timedelta
from collections import Counter
import pytz

from main import API_KEY, API_USER, API_URL

# Constants for the Last.fm API
# API_KEY = 'YOUR_LAST_FM_API_KEY'  # Replace with your API key from Last.fm
# USER = 'YOUR_LAST_FM_USERNAME'  # Replace with your Last.fm username
# BASE_URL = 'http://ws.audioscrobbler.com/2.0/'


def download_scrobbles(api_key, user):
    """
    Download scrobbles from the Last.fm API for the last three days for the specified user.
    """
    # Calculate date range: from 3 days ago until now
    end_date = datetime.now(pytz.timezone('Europe/Berlin'))
    start_date = end_date - timedelta(days=3)
    print(f'start_date: {start_date}')
    print(f'end_date:{end_date}')

    # Convert dates to UNIX timestamp format
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # API request parameters
    params = {
        'method': 'user.getrecenttracks',
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'from': start_timestamp,
        'to': end_timestamp,
        'limit': 200  # Assuming we don't need pagination for this task
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def count_scrobbles_by_day(scrobbles_data):
    """
    Count the number of scrobbles for each day from the JSON data provided by Last.fm.
    """
    scrobbles = scrobbles_data.get('recenttracks', {}).get('track', [])

    # Extract dates from scrobbles and count per day
    dates = [datetime.utcfromtimestamp(int(track['date']['uts'])).strftime('%Y-%m-%d') for track in scrobbles if
             'date' in track]
    counts_by_day = Counter(dates)

    return counts_by_day


# Execute the download and counting process
scrobbles_data = download_scrobbles(API_KEY, API_USER)
counts_by_day = count_scrobbles_by_day(scrobbles_data)

# Output the results
for day, count in counts_by_day.items():
    print(f"Date: {day}, Scrobbles: {count}")
