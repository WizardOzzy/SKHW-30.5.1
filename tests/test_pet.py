import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def test_get_all_pet(my_pets):
    '''Находим всех питомцев пользователя'''

    wait = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    stat = int(pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text.split()[2])

    wait = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    assert stat == len(pets)


def test_half_pet_photo(my_pets):
    '''Поверка того, что на странице "Мои питомцы" хотя бы у половины питомцев есть фото'''

    wait = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left')))

    stat = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    number = stat[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    half = number // 2

    number_of_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_photos += 1

    assert number_of_photos >= half
    print(f'Количество фото: {number_of_photos}')
    print(f'Половина от числа питомцев: {half}')


def test_pets_have_name_age_breed(my_pets):
    '''Проверяем есть ли у всех петов пользователя имя возраст порода'''
    pytest.driver.implicitly_wait(5)

    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result == 3


def test_all_pets_have_different_names(my_pets):
    '''Поверка того, что на странице "Мои питомцы" у всех питомцев разные имена'''

    wait = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])

    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(r)
    print(pets_name)


def test_no_duplicate_pets(my_pets):
    """Проверяем отсутствие дубликата питомцев (имя, порода, возраст)"""
    pytest.driver.implicitly_wait(5)
    # все имена
    names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

    pytest.driver.implicitly_wait(5)
    # все породы
    breeds = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')

    pytest.driver.implicitly_wait(5)
    # все возрасты
    ages = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

    # Создаем пустой список и счетчик
    pets = []
    r = 0
    print()

    for i in range(len(names)):
        # Собираем полученные данные в массив
        pets.append({
            'name': names[i].text,
            'breed': breeds[i].text,
            'age': ages[i].text
        })

        print('pets[', str(i), ']=', pets[i])

        # проверяем количество питомцев с такими же данными среди имеющихся элементов
        # при повторе питомца выходим из цикла
        r = pets.count(pets[i])
        print('количество вхождений =', str(r))
        if r != 1:
            break

    assert r == 1