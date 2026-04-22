# Запуск проекта

## Требования
- Python 3.11+
- PostgreSQL 14+

## Установка
1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте базу данных PostgreSQL `salon_booking` и пользователя.
4. Задайте переменные окружения (или используйте значения по умолчанию):
   ```bash
   set DJANGO_DB_NAME=salon_booking
   set DJANGO_DB_USER=postgres
   set DJANGO_DB_PASSWORD=postgres
   set DJANGO_DB_HOST=localhost
   set DJANGO_DB_PORT=5432
   ```
5. Выполните миграции и создайте администратора:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Запустите проект:
   ```bash
   python manage.py runserver
   ```

## Документация разработчика
1. Установите mkdocs и mkdocstrings:
   ```bash
   pip install mkdocs mkdocstrings[python] mkdocs-material
   ```
2. Соберите документацию:
   ```bash
   mkdocs build -f docs/mkdocs.yml
   ```