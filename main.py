import requests

URL = 'https://api.pokemonbattle.ru/v2'
TOKEN = 'db4faec70a0117c893de42aacc107632'
HEADER = {'Content-Type' : 'application/json', 'trainer_token':TOKEN}

body_change = {
    "pokemon_id": "252287",
    "name": "woobat",
    "photo_id": 6
}

body_catch = {
    "pokemon_id": "252297"
}



response_change = requests.put(url = f'{URL}/pokemons', headers = HEADER, json = body_change)
print(response_change.text)

response_catch = requests.post(url = f'{URL}/trainers/add_pokeball', headers = HEADER, json = body_catch)
print(response_catch.text)