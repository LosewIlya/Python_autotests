import pytest


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# каждый тест должен начинаться с test_


def test_positive_visit(browser):
    """
    Test case POC-1
    """
# определяем адрес страницы для теста и переходим на неё
    Url = "https://losewilya.github.io/"
    browser.get(url=Url)
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="contact"]')))
    browser.get(Url)
    element = browser.find_element(By.CSS_SELECTOR, '[class="contact"]')
    actual_text = 'Связаться со мной Email: losew.ilya2011@yandex.by'
    actual_text == element.text