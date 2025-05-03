
# Django Проект "Менеджер задач"

# Структура проекта

```
taskmanager/
├── core/                   # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tasks/                  # Приложение задач
│   ├── admin.py
│   ├── apps.py
│   ├── models/
│   │   ├── __init__.py     # Импорт моделей
│   │   ├── task.py         # Модель Task
│   │   └── subtask.py      # Модель SubTask
│   ├── migrations/
│   ├── views.py
│   └── ...
├── manage.py
└── venv/
```

# Установка и запуск проекта

```bash
# 1. Создание виртуального окружения
python -m venv venv
source venv/bin/activate 

# 2. Установка Django
pip install django

# 3. Создание проекта и приложения
mkdir taskmanager
cd taskmanager
django-admin startproject core .
python manage.py startapp tasks

# 4. Создание структуры моделей
mkdir tasks/models
touch tasks/models/task.py tasks/models/subtask.py tasks/models/__init__.py
rm tasks/models.py  # удалить стандартный models.py

# 5. Регистрация приложения в settings.py
# core/settings.py → INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    'tasks',
]

# 6. Создание и применение миграций
python manage.py makemigrations
python manage.py migrate

# 7. Создание суперпользователя
python manage.py createsuperuser

# 8. Запуск проекта
python manage.py runserver
```

# Работа с github

```
# создаем файл taskmanager/.gitignore

# подключаемся к github
git init
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/tsurkanOdessa/hw11.git
```

# Альтернативная админка Grappelli

```
1. Добавить в INSTALLED_APPS в settings.py перед django.contrib.admin
'grappelli',

2. В core/urls.py:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]

3.
pip install django-grappelli

```
