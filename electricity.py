import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Получаем последние данные о стоимости электричества
def get_latest_electricity_data():
    driver = webdriver.Chrome(service=Service(), options={})
    url = 'https://time2save.ru/tarify-na-elektroenergiu-dla-malih-predpriyatiy-i-ip'
    try:
        driver.get(url)
        time.sleep(20)
        table = driver.find_element(By.CLASS_NAME, 'table_title')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        data = {}
        for row in rows[2:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) > 0:
                region = cells[0].text.strip()
                price = float(cells[-2].text.strip().replace(',', '.'))
                data[region] = round(price, 2)
        return data
    except Exception as e:
        print("Ошибка при парсинге электричества:", e)
        return {}
    finally:
        driver.quit()

# Загружаем данные из файла
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Сохраняем обновленные данные в файл
def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Обновляем данные электричества
def update_electric_data():
    data = load_data()
    latest_electric_data = get_latest_electricity_data()

    for entry in data:
        if entry['region'] in latest_electric_data:
            entry['electric_price'] = latest_electric_data[entry['region']]
            entry['calc_value_4'] = round(entry['electric_price'] * 20.6, 2)  # Перерасчёт для 100 км

    save_data(data)

if __name__ == '__main__':
    update_electric_data()
