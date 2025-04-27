# Backend

## Создание миграций Alembic

### Инициализация

```bash
alembic init -t async migration
```

После выполнения этой команды в корне проекта появится директория migration и файл alembic.ini. Директория migration будет содержать файлы для управления миграциями, а alembic.ini — файл конфигурации Alembic, который потребуется нам для настройки подключения к базе данных.

### Подготовка файла миграций

```bash
alembic revision --autogenerate -m "Initial revision"
```

### Обновление базы данных до последней версии миграции

```bash
alembic upgrade head
```

[Асинхронный SQLAlchemy 2: простой пошаговый гайд по настройке, моделям, связям и миграциям с использованием Alembic](https://habr.com/ru/companies/amvera/articles/849836/)

[Асинхронный SQLAlchemy 2: пошаговый гайд по управлению сессиями, добавлению и извлечению данных с Pydantic](https://habr.com/ru/companies/amvera/articles/850470/)

## Генерация ключей

### Private
```bash
openssl genrsa -out jwt_private.pem 2048
```
### Public
```bash
openssl rsa -in jwt_private.pem -outform PEM -pubout -out jwt_public.pem
```
