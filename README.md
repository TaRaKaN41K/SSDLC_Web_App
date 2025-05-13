# Запуск

1. Клонировать репозиторий
2. Положить `.env` файлы в папку проекта, в папку `backend` и `frontend`
3. Собрать контейнеры 
```commandline
docker-compose up -d
```

## Адресс сайта 

Запускать через Chrome

https://0.0.0.0:3000/

## Адресс интерактивной документации к API
http://0.0.0.0:8000/docs#/


## Примеры `.env` файлов

### backend/.env
```.dotenv
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
CORS_ORIGINS="<белый список адресстов фронта через запятую без пробелов>"
```
### frontend/.env
```.dotenv
VITE_API_URL=<адресс API>
```

### /.env
```.dotenv
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DB_HOST=
DB_PORT=
```
