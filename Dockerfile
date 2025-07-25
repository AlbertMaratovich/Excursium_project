FROM python:3.13-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    openjdk-17-jre \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxshmfence1 \
    libvulkan1 \
    chromium \
    chromium-driver \
    xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка Allure CLI
ARG ALLURE_VERSION=2.25.0
RUN wget -q "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf "allure-${ALLURE_VERSION}.tgz" -C /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}/bin/allure" /usr/bin/allure

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Установка переменных окружения
ENV DISPLAY=:99

# Запуск тестов
CMD ["sh", "-c", "xvfb-run python -m pytest --alluredir=allure-results"]