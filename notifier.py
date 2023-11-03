import sys

from duplicates import parse_scrobble_date
from main import download_all_scrobbles, API_KEY, API_USER, start_ts, end_ts

def process_scrobbles(scrobles):
    sorted_scrobbles = []
    # Populate the list with scrobbles including their parsed dates
    for scrobble in scrobbles:
        scrobble_date_str = scrobble.get('date', {}).get('#text', None)
        scrobble_date = parse_scrobble_date(scrobble_date_str)
        if scrobble_date:  # Only consider scrobbles with a valid date
            sorted_scrobbles.append({
                'artist': scrobble['artist']['#text'],
                'track': scrobble['name'],
                'date': scrobble_date
            })

    # Sort scrobbles by date
    sorted_scrobbles.sort(key=lambda x: x['date'])

    # List to hold the duplicates
    duplicates = []

    # Check for duplicates within 20 minutes
    for i in range(len(sorted_scrobbles)):
        for j in range(i + 1, len(sorted_scrobbles)):
            # Break the inner loop if the next scrobble is beyond 20 minutes
            if (sorted_scrobbles[j]['date'] - sorted_scrobbles[i]['date']).total_seconds() > 1200:
                break
            # Check if the scrobbles have the same artist and track
            if sorted_scrobbles[i]['artist'].lower() == sorted_scrobbles[j]['artist'].lower() and \
                    sorted_scrobbles[i]['track'].lower() == sorted_scrobbles[j]['track'].lower():
                duplicates.append(sorted_scrobbles[j])

    if len(duplicates) > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    scrobbles = download_all_scrobbles(API_KEY, API_USER, start_ts, end_ts)
    result = process_scrobbles(scrobbles)
    if result:
        sys.exit(1)
    else:
        sys.exit(0)