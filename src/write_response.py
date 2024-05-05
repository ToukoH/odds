import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
sport = "baseball_mlb"
regions = "us"
markets = "h2h"
url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions={regions}&markets={markets}"

path = "../files/"
file = "odds.json"
complete_file = os.path.join(path, file)

res = requests.get(url)

if res.status_code == 200:
    data = res.json()
    print(data)
    with open(complete_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Written to {complete_file}")
else:
    print(f"Failed to retrieve data: {res.status_code}")
    with open(complete_file, 'w') as file:
        file.write("Error")
