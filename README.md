# course-site
Flask-based python task autochecker

## Локальный запуск

1. Создайте и активируйте виртуальное окружение (опционально, но желательно).
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Установите зависимости.
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите дев-сервер Flask.
   ```bash
   python -m flask --app project:create_app run --debug
   ```
   Приложение поднимется на `http://127.0.0.1:5000`. При первом запуске автоматически создастся база `instance/db.sqlite`.

### Создание администратора
Чтобы получить доступ к админке, создайте суперпользователя через Click-команду:
```bash
python -m flask --app project:create_app create-superuser
```
