import json


def get_task_file(lesson):
    """Возвращает нужный файл с задачами"""
    with open(f'project/tasks/tasks_{lesson}.json', encoding='utf-8') as f:
        file = json.load(f)
    return file