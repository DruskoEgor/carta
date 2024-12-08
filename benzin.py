import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Логин и пароль для доступа
username = 'leidark777@gmail.com'
password = 'lei777dark'

# Получаем последние данные о бензине
def get_latest_benzin_data(existing_data):
    latest_prices = {region['id']: region for region in existing_data}

    driver = webdriver.Chrome(service=Service(), options={})
    try:
        driver.get("https://www.benzin-price.ru/account.php")
        username_field = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='login']"))
        )
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='ok']"))
        )
        login_button.click()

        time.sleep(5)

        for region_id in range(1, 6):  # Поменяйте диапазон по нужде
            region_url = f'https://www.benzin-price.ru/stat_month.php?region_id={region_id}'
            driver.get(region_url)
            time.sleep(10)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'cellpadding': '5', 'cellspacing': '1', 'border': '0'})

            if table:
                rows = table.find_all('tr')
                last_valid_data = None

                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) > 4:
                        ai_95_price = cells[4].get_text().strip()
                        try:
                            ai_95_price = float(ai_95_price.replace(',', '.'))
                            if ai_95_price > 0:
                                last_valid_data = {"ai_95_price": ai_95_price}
                        except ValueError:
                            continue

                if last_valid_data:
                    calc_value_3 = last_valid_data["ai_95_price"] * 8
                    existing_entry = next((entry for entry in existing_data if entry['id'] == region_id), None)
                    calc_value_4 = existing_entry['calc_value_4'] if existing_entry else 0
                    latest_prices[region_id] = {
                        "id": region_id,
                        "region": existing_data[region_id - 1]["region"],
                        "ai_95_price": last_valid_data["ai_95_price"],
                        "electric_price": existing_data[region_id - 1]["electric_price"],
                        "calc_value_3": calc_value_3,
                        "calc_value_4": calc_value_4,
                        "source": "ИСТИНА"
                    }
    except Exception as e:
        print(f"Ошибка при авторизации или соединении: {e}")
    finally:
        driver.quit()

    return list(latest_prices.values())

# Загружаем данные из файла
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Сохраняем обновленные данные в файл
def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Обновляем данные бензина
def update_benzin_data():
    data = load_data()
    latest_data = get_latest_benzin_data(data)

    for entry in data:
        updated_entry = next((item for item in latest_data if item['id'] == entry['id']), None)
        if updated_entry:
            entry['ai_95_price'] = updated_entry['ai_95_price']
            entry['calc_value_3'] = updated_entry['calc_value_3']
            entry['source'] = updated_entry['source']

    save_data(data)

if __name__ == '__main__':
    update_benzin_data()
