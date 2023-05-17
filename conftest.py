import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import *


@pytest.fixture(autouse=True)
def my_pets():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Устанавливаем пользовательское разрешение экрана
    pytest.driver.set_window_size(1920, 1080)
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку мои питомцы
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()
    # Проверяем что мы на нужной странице
    assert pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-outline-success')

    yield

    pytest.driver.quit()

