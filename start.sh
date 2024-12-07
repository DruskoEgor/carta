#!/bin/bash

# Обновляем пакеты и устанавливаем Chromium и ChromeDriver
echo "Устанавливаем Chromium и ChromeDriver..."

# Обновляем apt и устанавливаем необходимые пакеты
apt-get update -y
apt-get install -y wget curl unzip chromium

# Скачиваем и устанавливаем ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp
unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/
rm /tmp/chromedriver_linux64.zip

# Убедитесь, что chromedriver доступен
chromedriver --version
chromium --version

# Устанавливаем виртуальное окружение для Python
python3 -m venv /opt/render/project/src/.venv
source /opt/render/project/src/.venv/bin/activate

# Устанавливаем зависимости Python
pip install -r /opt/render/project/src/requirements.txt

chmod +x start.sh

