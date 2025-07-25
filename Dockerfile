# FROM python:3.13.0-slim
FROM python:3.13-alpine

# Установка системных пакетов (для браузера и allure)
RUN apk update && apk add --no-cache \
    chromium \
    chromium-chromedriver \
    openjdk11-jre \
    xvfb \
    bash \
    dbus \
    ttf-freefont \
    tzdata \
    wget \
    curl \
    unzip

# Устанавливаем Allure CLI (можно менять версию через ARG)
ARG ALLURE_VERSION=2.25.0
RUN wget -q "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf "allure-${ALLURE_VERSION}.tgz" -C /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}/bin/allure" /usr/bin/allure

# Установка Allure CLI
#RUN wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz \
    #&& tar -xzf allure-2.25.0.tgz -C /opt/ \
    #&& ln -s /opt/allure-2.25.0/bin/allure /usr/bin/allure

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Устанавливаем переменную среды для xvfb-run
ENV CHROME_BIN=/usr/bin/chromium-browser \
    DISPLAY=:99

# Команда по умолчанию — запуск тестов и генерация директории результатов
# (далее сюда будет подкинуты результаты предыдущих тестов с гита и затем сгенерирован отчет)
CMD ["sh", "-c", "xvfb-run python -m pytest --alluredir=allure-results"]