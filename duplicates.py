import json
from datetime import datetime

# Function to convert the scrobble timestamp to a datetime object
def parse_scrobble_date(date_str):
    if date_str:
        return datetime.strptime(date_str, '%d %b %Y, %H:%M')
    return None

# Read the scrobbles from the file
with open('scrobbles.json', 'r') as infile:
    scrobbles = json.load(infile)

# List to hold all scrobble timestamps for comparison
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
    for j in range(i+1, len(sorted_scrobbles)):
        # Break the inner loop if the next scrobble is beyond 20 minutes
        if (sorted_scrobbles[j]['date'] - sorted_scrobbles[i]['date']).total_seconds() > 1200:
            break
        # Check if the scrobbles have the same artist and track
        if sorted_scrobbles[i]['artist'].lower() == sorted_scrobbles[j]['artist'].lower() and \
           sorted_scrobbles[i]['track'].lower() == sorted_scrobbles[j]['track'].lower():
            duplicates.append(sorted_scrobbles[j])

# HTML Report Generation
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Duplicate Scrobbles Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h2>Duplicate Scrobbles Report</h2>
    <table>
        <thead>
            <tr>
                <th>Artist</th>
                <th>Track</th>
                <th>Date Scrobbled</th>
            </tr>
        </thead>
        <tbody>
"""

# Add duplicate scrobbles to the HTML content
for dup in duplicates:
    html_content += f"""
            <tr>
                <td>{dup['artist']}</td>
                <td>{dup['track']}</td>
                <td>{dup['date'].strftime('%d %b %Y, %H:%M')}</td>
            </tr>
"""

# Finish the HTML content
html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Write the HTML content to a file
with open('duplicates_report.html', 'w') as html_file:
    html_file.write(html_content)

print('HTML report generated successfully: duplicates_report.html')
