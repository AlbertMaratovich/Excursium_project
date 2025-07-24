FROM python:3.13.0-slim

# Установка системных пакетов (для браузера и allure)
RUN apt-get update && apt-get install -y \
    unzip curl wget gnupg default-jre xvfb chromium chromium-driver \
    && apt-get clean

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

# Копируем предыдущую историю прогонов
RUN mkdir -p allure-report/history
COPY ./history ./allure-report/history || true

# Команда по умолчанию — запуск тестов и генерация отчета
CMD xvfb-run python -m pytest --alluredir=allure-results; \
    allure generate allure-results -o allure-report --clean || echo "Allure report not generated"; \
    cp -r allure-report/history ./history || echo "No history to save"