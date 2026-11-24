FROM python:3.11-slim AS builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#Финальный легковесный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные на первом этапе библиотеки
COPY --from=builder /install /usr/local

# Копируем исходный код приложения
COPY . .

EXPOSE 8080

CMD ["uvicorn", "cmd.app.main:app", "--host", "0.0.0.0", "--port", "8080"]