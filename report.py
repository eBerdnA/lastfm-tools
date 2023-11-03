import json

# Read the scrobbles from the file
with open('scrobbles.json', 'r') as infile:
    scrobbles = json.load(infile)

# Start of the HTML document
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Last.fm Scrobbles Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .header {
            padding: 10px 0;
            text-align: center;
            background-color: #333;
            color: white;
        }
        .header h1 {
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Last.fm Scrobbles Report</h1>
    </div>
    <div class="container">
        <table>
            <tr>
                <th>Artist</th>
                <th>Track</th>
                <th>Album</th>
                <th>Date Scrobbled</th>
            </tr>
"""

# Add each scrobble to the HTML table
for scrobble in scrobbles:
    artist_name = scrobble['artist']['#text']
    track_name = scrobble['name']
    album_name = scrobble['album']['#text']
    scrobble_date = scrobble.get('date', {}).get('#text', 'N/A')

    # Create a table row for each scrobble
    html += f"""
            <tr>
                <td>{artist_name}</td>
                <td>{track_name}</td>
                <td>{album_name}</td>
                <td>{scrobble_date}</td>
            </tr>
    """

# End of the HTML document
html += """
        </table>
    </div>
</body>
</html>
"""

# Write the HTML content to a file
with open('scrobbles_report.html', 'w') as htmlfile:
    htmlfile.write(html)

print('HTML report generated successfully: scrobbles_report.html')
