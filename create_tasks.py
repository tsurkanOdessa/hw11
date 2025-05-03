import requests
import json
from datetime import datetime, timedelta
import random

# Базовый URL API
BASE_URL = "http://localhost:8000/api/"

# Возможные статусы задач
TASK_STATUSES = ["new", "in_progress", "completed"]


def create_task(task_data):
    """Создает новую задачу через API"""
    response = requests.post(f"{BASE_URL}tasks/create/", json=task_data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Ошибка при создании задачи: {response.status_code}")
        print(response.text)
        return None


def create_subtask(subtask_data):
    """Создает подзадачу через API"""
    response = requests.post(f"{BASE_URL}subtasks/", json=subtask_data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Ошибка при создании подзадачи: {response.status_code}")
        print(response.text)
        return None


def generate_tasks():
    """Генерирует 11 задач с подзадачами"""
    for i in range(1, 12):  # Создаем 11 задач
        # Основные данные задачи
        task_title = f"Задача №{i}"
        deadline = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        status = random.choice(TASK_STATUSES)

        task_data = {
            "title": task_title,
            "description": f"Описание задачи №{i}. Это автоматически сгенерированная задача.",
            "status": status,
            "deadline": deadline
        }

        # Создаем задачу
        task = create_task(task_data)
        if not task:
            continue

        print(f"Создана задача: {task['title']} (ID: {task['id']}), статус: {task['status']}")

        # Создаем подзадачи для этой задачи
        subtasks_count = random.randint(1, 4)  # От 1 до 4 подзадач
        for j in range(1, subtasks_count + 1):
            is_done = random.choice([True, False]) if status == 'completed' else False

            subtask_data = {
                "title": f"Подзадача {j} для задачи №{i}",
                "is_done": is_done,
                "task": task['id']  # Связываем подзадачу с задачей
            }

            subtask = create_subtask(subtask_data)
            if subtask:
                print(
                    f"  -> Создана подзадача: {subtask['title']} (ID: {subtask['id']}), выполнена: {subtask['is_done']}")


if __name__ == "__main__":
    print("Начало создания задач...")
    generate_tasks()
    print("Готово!")