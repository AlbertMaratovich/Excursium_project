# FROM python:3.13.0-slim
FROM python:3.13.5

# Установка системных пакетов (для браузера и allure)
RUN apt-get update && apt-get install -y \
    unzip curl wget gnupg default-jre xvfb \
    && apt-get clean

RUN CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1-3) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Установка браузера хром
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Установка Allure CLI
RUN wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz \
    && tar -xzf allure-2.25.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.25.0/bin/allure /usr/bin/allure

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Устанавливаем переменную среды для xvfb-run
ENV DISPLAY=:99

# Команда по умолчанию — запуск тестов и генерация директории результатов
# (далее сюда будет подкинуты результаты предыдущих тестов с гита и затем сгенерирован отчет)
CMD ["sh", "-c", "xvfb-run python -m pytest --alluredir=allure-results"]