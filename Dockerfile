# Используем официальный Python-образ
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libasound2 \
    libgtk-3-0 \
    libgbm-dev \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libatk1.0-0 \
    libpangocairo-1.0-0 \
    libxinerama1

# Устанавливаем Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || true \
    && apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Устанавливаем ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Устанавливаем Python-зависимости
RUN pip install selenium
RUN pip install flask
# Копируем ваш код
COPY . /app
WORKDIR /app
RUN which google-chrome
RUN google-chrome --version
RUN which chromedriver
RUN chromedriver --version
ENV PATH="/usr/bin:$PATH"


# Указываем команду для запуска приложения
CMD ["python", "app.py"]
