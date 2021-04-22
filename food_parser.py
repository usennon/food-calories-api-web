import requests
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ENDPOINT = 'https://api.edamam.com/api/food-database/v2/parser'
APP_ID = os.getenv(key='API_ID')
APP_KEY = os.getenv(key='API_KEY')

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "ingr": None
}


def get_food_data(ingr="apple"):
    params["ingr"] = ingr
    response = requests.get(url=ENDPOINT, params=params)
    return response.json()

