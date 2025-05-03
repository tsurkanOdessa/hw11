
# Django Проект "Менеджер задач"

# Структура проекта

```
taskmanager/
├── core/                   # настройки Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tasks/                  # приложение задач
│   ├── admin.py
│   ├── apps.py
│   ├── models/
│   │   ├── __init__.py     # импорт всех моделей
│   │   ├── task.py         # модель Task
│   │   └── subtask.py      # модель SubTask
│   ├── templates
│   │   ├── task_list.html  # шаблон главной страницы
│   ├── migrations/
│   ├── views.py
│   ├── urls.py
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
# установка и настройка Django REST Framework

```
pip install djangorestframework

Добавить в INSTALLED_APPS в settings.py
INSTALLED_APPS = [
    ...
    'tasks',
    'rest_framework', # Добавим строку
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
```