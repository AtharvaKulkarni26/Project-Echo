import requests
import json
import os
import csv

FREESOUND_API_URL = "https://freesound.org/apiv2/"
API_KEY = "your api key"  # Replace with your API key

DOWNLOAD_FOLDER = 'downloaded_sounds'
CSV_FILE = 'sound_details.csv'

def get_water_sounds(query, limit=10):
    params = {
        "query": query,
        "token": API_KEY,
        "fields": "id,name,previews",  # get id, name, and preview links
        "page_size": limit
    }

    response = requests.get(FREESOUND_API_URL + "search/text/", params=params)
    response_data = json.loads(response.text)

    if "results" in response_data:
        # Create the download folder if it doesn't exist
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.mkdir(DOWNLOAD_FOLDER)

        # Open CSV for writing
        with open(CSV_FILE, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Name', 'Preview URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in response_data["results"]:
                print(f"ID: {result['id']}, Name: {result['name']}")
                print(f"Preview URL: {result['previews']['preview-hq-mp3']}")
                print("-" * 50)

                # Download the sound
                sound_url = result['previews']['preview-hq-mp3']
                sound_name = os.path.join(DOWNLOAD_FOLDER, f"{result['id']}_{result['name']}.mp3")
                with open(sound_name, 'wb') as sound_file:
                    sound_response = requests.get(sound_url)
                    sound_file.write(sound_response.content)

                # Write details to CSV
                writer.writerow({
                    'ID': result['id'],
                    'Name': result['name'],
                    'Preview URL': sound_url
                })

if __name__ == "__main__":
    get_water_sounds("ocean", limit=50)
