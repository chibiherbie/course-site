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
        print(count_task_user)
        return render_template('admin.html', len_users=len(users), len_tasks=len(tasks), users=users,
                               count_task_user=count_task_user)
    return redirect(url_for('main.index'))


@admin.route('/admin/<int:user_id>')
@login_required
def info_user(user_id):
    if current_user.is_admin():
        users = User.query.filter_by().all()
        tasks = Tasks.query.filter_by().all()

        count_task_user = {}
        for user in users:
            count_task_user[user.id] = len(Tasks.query.filter_by(user_id=user.id).all())
        print(user_id)
        return render_template('admin.html', len_users=len(users), len_tasks=len(tasks), users=users,
                               count_task_user=count_task_user)
    return redirect(url_for('main.index'))
