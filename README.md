# Блогикум — финальный проект шестого спринта

Учебный Django-проект: публикации, профили, комментарии, изображения,
пагинация и управление доступом. В основу положен проект пятого спринта

## Запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd blogicum
python manage.py migrate
python manage.py loaddata ../db.json
python manage.py createsuperuser
python manage.py runserver
```

На windows окружение активируется командой `venv\Scripts\activate`.
Фикстуры необязательны. Суперпользователь создается самостоятельно

## Проверка

Из корня репозитория:

```bash
pytest
```

Локально пройдены 26 тестов: профили, права авторов, создание,
редактирование и удаление записей и комментариев, скрытые и отложенные
публикации, пагинация, изображения, страницы ошибок, настройки почты

Письма сохраняются в `blogicum/sent_emails/`, изображения — в
`blogicum/media/`. Каталоги и БД не включены в git
