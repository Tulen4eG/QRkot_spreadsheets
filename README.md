# API в поддержку котиков

## Описание

Этот проект предназначен для доната на кошачие нужды.

### Возможности проекта:
- Cоздание благотворительных проектов.
- Cоздание и автоматическое распределение между проектами пожертвований от пользователей.
- Создание нового суперпользователя при первом запуске проекта.
- Управление пользователями.
- Формирование отчёта в гугл-таблице. В ней указаны закрытые проекты, отсортированные по скорости сбора средств.

## Технологии
- Python 3.9
- Alembic 1.7.7
- Sqlalchemy 1.4.36
- Uvicorn-standard 0.17.6
- FastAPI 0.78.0
- Aiogoogle 4.2.0
- Google Drive API v3
- Google Sheets API v4
- Pytest

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/Tulen4eG/QRkot_spreadsheets
   ```
2. Перейти в папку:
   ```
   cd cat_charity_fund
   ```
3. Создайте виртуальное окружение.
4. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
5. Создайте файл .env как минимум с переменными:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
   SECRET=secretpassword
   ```
   Для Google Sheets отчета:
   cоздайте проект в [Google Cloud Platform](https://console.cloud.google.com/projectselector2/home/dashboard), добавьте сервисный аккаунт и подключите API - Google Drive и Google Sheets.
   Данные из Json скопируйте в .env:
   ```
   TYPE=...
   PROJECT_ID=...
   PRIVATE_KEY_ID=...
   PRIVATE_KEY="..."
   CLIENT_EMAIL=...
   CLIENT_ID=...
   AUTH_URI=...
   TOKEN_URI=...
   AUTH_PROVIDER_X509_CERT_URL=...
   CLIENT_X509_CERT_URL=...

   EMAIL=ваша_почта_для_доступа_к_таблице@gmail.com
   ```
6. Создайте бд:
   ```
   alembic upgrade head
   ```
   

## Запуск

Выполните команду:
```
uvicorn app.main:app
```

Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc

## Тестирование
Запустите тесты:
```
pytest
```

### Made by Tulen4eG & YandexPracticum
Николашин Тимофей
[telegram](https://t.me/Tulen4eg)
