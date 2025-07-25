# FROM python:3.13.0-slim
FROM python:3.13.5

# Установка системных пакетов (для браузера и allure)
RUN apt-get update && apt-get install -y \
    unzip curl wget gnupg default-jre xvfb \
    && apt-get clean

# Установка браузера хром
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
      | gpg --dearmor -o /usr/share/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] \
           http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Динамически получаем версию установленного Chrome и скачиваем matching Chromedriver
RUN CHROME_VER="$(google-chrome --version | grep -Po '\d+\.\d+\.\d+')" && \
    DRIVER_VER="$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VER})" && \
    wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VER}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

RUN google-chrome-stable --version

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