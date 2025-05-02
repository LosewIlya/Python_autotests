import requests
import pytest


URL = 'https://api.pokemonbattle.ru/v2'
TOKEN = 'db4faec70a0117c893de42aacc107632'
HEADER = {'Content-Type' : 'application/json', 'trainer_token':TOKEN}
TRAINER_ID = '32638'


def test_pokemons_id_trainers_name():
    response_json = requests.get(url = f'{URL}/pokemons', params = {'trainer_id' : TRAINER_ID}).json()
    assert response_json['data'][0]['trainer_id'] == TRAINER_ID and response_json['data'][0]['id'] == '299683' and response_json['data'][0]['name'] == 'Панда'

def test_status_code_trainers():
 response_get = requests.get(url = f'{URL}/trainers', params = {'trainer_id' : TRAINER_ID})
 assert response_get.status_code == 200


def test_status_name_id():
    response_json = requests.get(url = f'{URL}/trainers', params = {'trainer_id' : TRAINER_ID}).json()
    assert response_json['data'][0]['trainer_name'] == 'Elk'and response_json['data'][0]['id'] == TRAINER_ID 





