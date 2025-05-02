import pytest
import requests
from selenium import webdriver



from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
URL = 'https://pokemonbattle-stage.ru/'

def test_positive_login(browser):
    """
    TRP-1. Positive case
    """
   
    browser.get(URL)
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input k_form_f_email css-1pk1fka"]')
    email_input.click()
    email_input.send_keys('losew.ilya2011@yandex.by')

    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys('Elk356823')

    
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 k_form_send_auth css-cm2fpt"]')
    button.click()

    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
   
    trainer_id = browser.find_element(by=By.CSS_SELECTOR, value='[class="header_card_trainer_id"]')

    text_id = trainer_id.text.replace('\n', ' ')
    assert text_id == 'ID 2485', 'Unexpected trainer id'


CASES = [
    ('1', 'losew.ilya2011yandex.by', 'Elk356823', ['Введите корректную почту', '']),
    ('2', 'losew.ilya2011@yandex.by', 'Elk356821', ['', 'Неверные логин или пароль']),
    ('3', 'losew.ilya2011@yandex', 'Elk356821', ['Введите почту', '']),
    ('4', '', 'Elk356823', ['Введите почту', '']),
    ('5', 'losew.ilya2011@yandex.by', '', ['', 'Введите пароль'])
]

@pytest.mark.parametrize('case_number, email, password, alerts', CASES)

def test_negative_login(case_number, email, password, alerts, browser):
    """
    TRP-1. Negative cases
    """
    logger.info(f'CASE : {case_number}')
    browser.get(URL)
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/login'))

    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input k_form_f_email css-1pk1fka"]')
    email_input.click()
    email_input.send_keys(email)

    password_input = browser.find_element(by=By.ID, value='k_password')
    password_input.click()
    password_input.send_keys(password)

    
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 k_form_send_auth css-cm2fpt"]')
    button.click()

    alerts_messges = browser.find_elements(by=By.CSS_SELECTOR, value='[class="MuiFormHelperText-root Mui-error MuiFormHelperText-sizeMedium MuiFormHelperText-contained MuiFormHelperText-filled auth__error css-1kinjm4"]')
    
def test_check_api(browser, knockout):
    """
    TRP-3. Check create pokemon by api request
    """
    browser.get(url=URL)
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/login'))

    email = browser.find_element(By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input k_form_f_email css-1pk1fka"]')
    email.click()
    email.send_keys('losew.ilya2011@yandex.by')

    password = browser.find_element(by=By.ID, value='k_password')
    password.click()
    password.send_keys('Elk356823')

    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 k_form_send_auth css-cm2fpt"]')
    enter.click()
    
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    
    trainer_pick = browser.find_element(by=By.CSS_SELECTOR, value='[class="header_card_trainer style_1_interactive_button_link"]')
    trainer_pick.click()
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/trainer/2485'))

    pok = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[class*="pokemon_one_body_content_inner_pokemons"]')))
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        lambda x: 'feature-empty' not in pok.get_attribute('class'))
    
    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value='[class="total-count history-info_count"]')
    count_before = int(pokemon_count_before.text)

    body_create = {
        "name": "generate",
        "photo_id": 2
    }
    HEADER = {'Content-Type':'application/json','trainer_token':'0769c129223f3630de4eb1888f3afd13'}
    response_create = requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons', headers=HEADER, json=body_create, timeout=3)
    assert response_create.status_code == 201, 'Unexpected response status_code'

    browser.refresh()
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/trainer/2485'))
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[class="total-count history-info_count"]')))


    assert WebDriverWait(browser, timeout=5, poll_frequency=1).until(
    EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '[class="total-count history-info_count"]'), str(count_before + 1))), 'Unexpected pokemons count'


# каждый тест должен начинаться с test_
def test_positive_login_wiki(browser):
    """
    Test case POC-1
    """
	# определяем адрес страницы для теста и переходим на неё
    url = "https://pokemonbattle.ru/"
    browser.get(url=url)

	# ищем по селектору инпут "Email", кликаем по нему и вводим значение email
    email = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="k_form_control"] [id="k_email"]')))
    email.click()
    email.send_keys('losew.ilya2011@yandex.by')
    # email.send_keys('user@mail.com') # введи тут email своего тестового аккаунта на prod окружении

	# ищем по селектору инпут "Password", кликаем по нему и вводим значение пароля
    password = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_control"] [id="k_password"]')
    password.click()
    password.send_keys('Elk356823') # введи тут пароль своего тестового аккаунта на prod окружении

	# ищем по селектору кнопку "Войти" и кликаем по ней
    enter = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_send_auth"]')
    enter.click()

    # ждем успешного входа и обновления страницы
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be(url))

	# ищем элемент на странице, который содержит ID тренера
    trainer_id = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="header_card_trainer_id_num"]')))

	# сравниваем полученный ID из кода теста с ID вашего тестового тренера
    assert trainer_id.text == '32638', 'Unexpected ID trainer' # введи тут ID своего тренера    