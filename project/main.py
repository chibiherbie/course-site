import json
import operator
import time
from threading import Thread

from flask import request

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .utils import get_task_file
from . import db
from .models import Tasks, User

from .check_task import start_check, run, check_task
from concurrent.futures import ThreadPoolExecutor


main = Blueprint('main', __name__)

executor = ThreadPoolExecutor(1)


@main.route('/', methods=['GET'])
def index():

    # TEST
    # executor.submit(run)

    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    tasks = Tasks.query.filter_by(user_id=current_user.id, completed=True).all()
    users = User.query.filter_by().all()
    uest_position = sorted(users, key=operator.attrgetter('money'), reverse=True).index(current_user) + 1
    return render_template('profile.html', name=current_user.name, tasks=len(tasks), money=current_user.money,
                           position=uest_position)


@main.route('/lessons')
@login_required
def lessons():
    return render_template('lesson.html', name=current_user.name)


@main.route('/lesson/<int:num_lesson>')
@login_required
def lesson(num_lesson):

    file = get_task_file(num_lesson)

    did_tasks = Tasks.query.filter_by(user_id=current_user.id, lesson=num_lesson).all()

    return render_template('task.html', name=current_user.name, lessons=file['tasks'],
                           count=len(file['tasks']), lesson=num_lesson,
                           did_tasks={i.task: did_tasks[num] for num, i in enumerate(did_tasks)})


# @main.route('/lesson')
# @login_required
# def back():
#
#     file = get_task_file(1)
#
#     return render_template('task.html', name=current_user.name, lessons=file['tasks'],
#                            count=len(file['tasks']), lesson=1)


@main.route('/task/<int:lesson>_<int:task>', methods=['GET'])
@login_required
def task_num(lesson, task):
    """Рендерим задачу"""

    file = get_task_file(lesson)

    task_user = Tasks.query.filter_by(user_id=current_user.id, lesson=lesson, task=task).first()
    text = task_user.text if task_user else ''

    tasks = file['tasks'][task]

    for num, i in enumerate(tasks['description']):
        tasks['description'][num] = i.replace('\n', '<br/>')

    for num, i in enumerate(tasks['data']):
        tasks['data'][num]['data_in'] = i['data_in'].replace('\n', '<br/>')
        tasks['data'][num]['data_out'] = i['data_out'].replace('\n', '<br/>')

    isLast = True if task + 1 < len(file['tasks']) else False

    return render_template('task_num.html', tasks=file['tasks'][task],
                           num=(task + 1), text=text, lesson=lesson, charset='utf8', isLast=isLast)



@main.route('/submit/<int:num_lesson>_<int:num_task>', methods=['POST'])
@login_required
def submit(num_lesson, num_task):
    """Добовляем решение задачи"""

    task = Tasks.query.filter_by(user_id=current_user.id, lesson=num_lesson, task=num_task).first()

    if task:
        # решение уже было
        task.text = request.form.get("form-text")
        task.is_check = True
        db.session.commit()

    else:
        # Новое решение
        task = Tasks(user_id=current_user.id, lesson=num_lesson, task=num_task, completed=None, is_check=True,
                     text=request.form.get("form-text"))
        db.session.add(task)
        db.session.commit()

    file = get_task_file(num_lesson)

    # start_check()
    # executor.submit(start_check)
    # start_check()
    # check_task({'text': task.text, "lesson": task.lesson, "task": task.task})

    isLast = True if num_task + 1 < len(file['tasks']) else False

    return render_template('task_num.html', tasks=file['tasks'][num_task],
                           num=(num_task + 1), text=request.form.get("form-text"), lesson=num_lesson,
                           answer='Решение отправлено', isLast=isLast, charset='utf8')


# @main.route('/get_users/<int:token>', methods=['GET'])
# def api_task(token):
#     """Меняем статус задачи"""
#     if token == 1423:
#         from flask import jsonify, json
#
#         user = User.query.filter_by().all()
#         print(json.dumps(user[0]))
#         print(jsonify(user[0]))
#         a = [{""} for i in user]
#         return {"users": response}
#     return {'result': "Ok"}
