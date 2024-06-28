FROM python:3.11.4-slim-buster

ENV HOST=0.0.0.0

ENV LISTEN_PORT 8080

EXPOSE 8080

# Устанавливаем wget и другие необходимые инструменты
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget build-essential gfortran libblas-dev liblapack-dev libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
RUN mkdir /app

# Копируем файлы приложения
COPY app_rag/ /app/app_rag/
COPY pyproject.toml /app/
COPY .env /app/
COPY .configs/ /app/.configs/

# Создаем директорию и загружаем сертификат
RUN mkdir -p /app/.opensearch/ && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
         --output-document /app/.opensearch/root.crt && \
    chmod 0600 /app/.opensearch/root.crt

WORKDIR /app

# Устанавливаем необходимые библиотеки
RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    poetry add openpyxl python-dotenv httpx[socks]

# Команда для запуска приложения
CMD ["poetry", "run", "python", "app_rag/app_rag_main.py"]
