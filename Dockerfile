FROM selenium/standalone-chrome:latest

USER root

# Установка Python 3 (достаточно 3.11/3.12 — не 3.13)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# Установка Allure CLI
ARG ALLURE_VERSION=2.25.0
RUN wget -q "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf "allure-${ALLURE_VERSION}.tgz" -C /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}/bin/allure" /usr/bin/allure

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем твой код
COPY . .

# Запуск тестов
CMD ["sh", "-c", "python -m pytest --alluredir=allure-results"]