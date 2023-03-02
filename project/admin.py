from flask import request, url_for

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .utils import get_task_file
from . import db
from .models import Tasks

from .check_task import start_check

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def index():
    if current_user.is_admin():
        return render_template('admin.html')
    return redirect(url_for('main.index'))
