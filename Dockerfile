FROM python:3.13-alpine
# update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add --no-cache chromium chromium-chromedriver tzdata

# Get all the prereqs
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk

RUN apk update && \
    apk add openjdk11-jre curl tar

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