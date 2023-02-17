from flask import request

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import json
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/task')
@login_required
def task():

    with open('project/tasks/tasks.json', encoding='utf-8') as f:
        file = json.load(f)

    for index, i in enumerate(file['lessons']['1']):
        print(i)
    return render_template('task.html', name=current_user.name, lessons=file['lessons']['1'],
                           count=len(file['lessons']['1']))


@main.route('/task/<int:num>', methods=['GET'])
@login_required
def task_num(num):
    with open('project/tasks/tasks.json', encoding='utf-8') as f:
        file = json.load(f)

    return render_template('task_num.html', lessons=file['lessons']['1'][num],
                           num=(num + 1))


@main.route('/submit', methods=['POST'])
def submit():
    print(request.form.get("form-text"))
    return 'You entered: {}'.format(request.form.get("form-text"))





