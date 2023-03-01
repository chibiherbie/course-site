from flask import request

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .utils import get_task_file
from . import db
from .models import Tasks

from .check_task import start_check

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    tasks = Tasks.query.filter_by(user_id=current_user.id, completed=True).all()

    return render_template('profile.html', name=current_user.name, tasks=len(tasks))


@main.route('/lessons')
@login_required
def lessons():
    return render_template('lesson.html', name=current_user.name)


@main.route('/lesson/<int:num_lesson>')
@login_required
def lesson(num_lesson):

    file = get_task_file(num_lesson)

    return render_template('task.html', name=current_user.name, lessons=file['tasks'],
                           count=len(file['tasks']), lesson=num_lesson)


@main.route('/lesson')
@login_required
def back():

    file = get_task_file(1)

    return render_template('task.html', name=current_user.name, lessons=file['tasks'],
                           count=len(file['tasks']), lesson=1)


@main.route('/task/<int:lesson>_<int:task>', methods=['GET'])
@login_required
def task_num(lesson, task):
    file = get_task_file(lesson)

    task_user = Tasks.query.filter_by(user_id=current_user.id, lesson=lesson, task=task).first()
    text = task_user.text if task_user else ''

    return render_template('task_num.html', tasks=file['tasks'][task],
                           num=(task + 1), text=text, lesson=lesson, charset='utf8')


@main.route('/submit/<int:num_lesson>_<int:num_task>', methods=['POST'])
@login_required
def submit(num_lesson, num_task):
    """Добовляем решение задачи"""

    task = Tasks.query.filter_by(user_id=current_user.id, lesson=num_lesson, task=num_task).first()

    if task:
        # решение уже было
        task.text = request.form.get("form-text")
        db.session.commit()

    else:
        # Новое решение
        task = Tasks(user_id=current_user.id, lesson=num_lesson, task=num_task, completed=False,
                     text=request.form.get("form-text"))
        db.session.add(task)
        db.session.commit()

    file = get_task_file(num_lesson)

    start_check(task)

    return render_template('task_num.html', tasks=file['tasks'][num_task],
                           num=(num_task + 1), text=request.form.get("form-text"), lesson=num_lesson,
                           answer='Решение отправлено')


@main.route('/api/change_task', methods=['POST'])
@login_required
def api_task():
    """Меняем статус задачи"""

    task = Tasks.query.filter_by(user_id=current_user.id, lesson=num_lesson, task=num_task).first()

    if task:
        # решение уже было
        task.text = request.form.get("form-text")
        db.session.commit()

    else:
        # Новое решение
        task = Tasks(user_id=current_user.id, lesson=num_lesson, task=num_task, completed=False,
                     text=request.form.get("form-text"))
        db.session.add(task)
        db.session.commit()

    return ""



