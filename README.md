# Электронная запись в салон красоты

Веб-приложение для автоматизации записи клиентов на услуги салона красоты.
Проект разработан на Django 5.x и соответствует требованиям дисциплины
«Системная и программная инженерия» (отчёты 1–8, ТЗ, архитектура, диаграммы).

## Команда
- **Группа:** ИКБО-14-23
- **Гиёсидинов И.** — руководитель проекта, разработчик
- **Комова Д.** — аналитик
- **Михеева Е.** — разработчик, дизайнер

## Стек
- Python 3.11+ / Django 5.x
- PostgreSQL
- Bootstrap 5
- MkDocs + mkdocstrings

## Возможности
- Регистрация/авторизация/восстановление пароля
- Клиент: выбор услуги → мастера → свободного времени → запись
- Отображение свободных слотов
- Личный кабинет клиента (история, отмена, перенос)
- Мастер: просмотр расписания
- Администратор: CRUD услуг, мастеров, слотов, просмотр всех записей
- Валидация доступности слотов

## Быстрый старт
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set DJANGO_DB_NAME=salon_booking
set DJANGO_DB_USER=postgres
set DJANGO_DB_PASSWORD=postgres
set DJANGO_DB_HOST=localhost
set DJANGO_DB_PORT=5432
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Документация разработчика
```bash
pip install mkdocs mkdocstrings[python] mkdocs-material
mkdocs build -f docs/mkdocs.yml
```

Готовая документация будет доступна в каталоге `docs/site/`.