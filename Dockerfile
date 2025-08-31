FROM python:3.11-alpine

WORKDIR /app

# Устанавливаем системные зависимости
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev \
    && apk add --no-cache libpq

# Копируем и устанавливаем Python зависимости
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Удаляем ненужные build-зависимости чтобы уменьшить размер image
RUN apk del .build-deps

# Копируем исходный код
COPY . .

ENV IS_DOCKER=DOCKER

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]