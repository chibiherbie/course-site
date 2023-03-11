# -*- coding: utf-8 -*-
from flask import Flask


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
# from .utils import make_celery

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.config['SECRET_KEY'] = 'YEEES_sibHub'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:5000/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:5000/0'
    app.config['threaded'] = True
    app.config['threaded'] = True

    db.init_app(app)

    # celery = make_celery(app)
    # celery.set_default()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    with app.app_context():
        db.create_all()

    @app.cli.command("create-superuser")
    def create_superuser():
        email = input('Insert email of superuser: ')
        password = input('Insert password of superuser: ')
        db.session.add(User(email=email, name='admin',
                            password=generate_password_hash(password, method='sha256'), super_user=True))
        db.session.commit()

    return app


if __name__ == "__main__":
    a, b = create_app()
    a.run(host='0.0.0.0', threaded=True)
