FROM python:3.12

WORKDIR /app

# Копируем зависимости отдельно для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь бэкенд
COPY . .

# Создаем директории для uploads и logs
RUN mkdir -p /app/uploads /app/logs /app/certs
RUN chmod -R 755 /app/uploads /app/logs

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
