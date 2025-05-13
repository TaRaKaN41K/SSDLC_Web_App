FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads /app/logs
RUN chmod -R 755 /app/uploads /app/logs

RUN mkdir -p /app/certs && \
    openssl genrsa -out /app/certs/jwt_private.pem 2048 && \
    openssl rsa -in /app/certs/jwt_private.pem -outform PEM -pubout -out /app/certs/jwt_public.pem

ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
