# Блогикум — публикации

Проект пятого спринта: модели публикаций, категорий и местоположений,
русская админ-зона, фильтрация по времени и статусу публикации.

Запуск:

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

Проверка из корня репозитория: `pytest`. Локально пройдены все 82 теста.
Проект предназначен для локальной учебной разработки.
