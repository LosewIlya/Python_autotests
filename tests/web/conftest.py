import pytest
import requests



from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



@pytest.fixture(scope='function')
def browser():
    """
    Basic fixture
    """
    chrome_options = Options()
    #chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    chrome_options.add_argument("--disable-search-engine-choice-screen") # отключаем выбор движка для поиска
    #chrome_options.add_argument("--headless") # спец. режим "без браузера"
    # устанавливаем webdriver в соответствии с версией используемого браузера
    service = Service()
    # запускаем браузер с указанными выше настройками
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def knockout():
    """
    Knockout all pokemons
    """
    header = {'Content-Type':'application/json','trainer_token': '0769c129223f3630de4eb1888f3afd13'}
    pokemons = requests.get(url=f'https://api.pokemonbattle-stage.ru/v2/pokemons/knockout', params={"trainer_id": 2485},
                            headers=header, timeout=3)
    if 'data' in pokemons.json():
        for pokemon in pokemons.json()['data']:
             if pokemon['status'] != 0:
                requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons/knockout', 
                              headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()  # Или Firefox(), Edge() и т.д.
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()

    