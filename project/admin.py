import operator

from flask import request, url_for

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .utils import get_task_file
from . import db
from .models import Tasks, User

from .check_task import start_check

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def index_admin():
    if current_user.is_admin():
        users = User.query.filter_by().all()
        tasks = Tasks.query.filter_by().all()

        count_task_user = {}
        for user in users:
            count_task_user[user.id] = len(Tasks.query.filter_by(user_id=user.id).all())

        return render_template('admin.html', len_users=len(users), len_tasks=len(tasks), users=users,
                               count_task_user=count_task_user)
    return redirect(url_for('main.index'))


@admin.route('/admin/<int:user_id>')
@login_required
def info_user(user_id):
    if current_user.is_admin():
        user = User.query.filter_by(id=user_id).first()
        tasks = Tasks.query.filter_by(user_id=user_id).all()

        return render_template('admin_profile.html', name=user.name, len_tasks=len(tasks), user=user,
                               tasks=sorted(tasks, key=operator.attrgetter('lesson')))
    return redirect(url_for('main.index'))


@admin.route('/admin/<int:lesson>_<int:task>_<int:user_id>', methods=['GET'])
@login_required
def info_task_user(lesson, task, user_id):
    """Рендерим задачу"""
    if current_user.is_admin():
        file = get_task_file(lesson)

        task_user = Tasks.query.filter_by(user_id=user_id, lesson=lesson, task=task).first()
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
    return redirect(url_for('main.index'))
