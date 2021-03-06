from functools import wraps
from todo_app.user.user import Roles, User
import flask_login
from todo_app.github.github_authentication import GithubAuthentication
from todo_app.mongo.mongo_wrapper import MongoWrapper
from flask import Flask, render_template, request, redirect, url_for
import os
from todo_app.models.view_model import ViewModel
from flask_login import LoginManager, login_required

from loggly.handlers import HTTPSHandler 
from logging import Formatter


def create_app(database_name="Main"):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["USER_UNAUTHORIZED_ENDPOINT"] = "/index"
    app.logger.setLevel(os.environ.get("LOG_LEVEL", default="INFO"))
    
    if os.environ.get('LOGGLY_TOKEN'):
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{os.environ.get("LOGGLY_TOKEN")}/tag/todo-app')    
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))    
        app.logger.addHandler(handler)
    
    mongo_database = MongoWrapper(os.environ.get('MONGO_URL'), database_name)
    login_manager = LoginManager()
    github_authenticator = GithubAuthentication()
    
    def roles_required(role_name):
        def wrapper(view_function):
            @wraps(view_function)    # Tells debuggers that is is a function wrapper
            def decorator(*args, **kwargs):
                if not flask_login.current_user.check_role(role_name):
                    app.logger.warning("User attempted to access page without required permission")
                    # Redirect to unauthenticated page
                    return redirect(url_for('index'))
                return view_function(*args, **kwargs)
            return decorator
        return wrapper

    @login_manager.unauthorized_handler
    def unauthenticated():
        app.logger.info("Authenticating with github")
        authentication_url = github_authenticator.get_github_auth_url()
        return redirect(authentication_url)
        
    
    @login_manager.user_loader
    def load_user(user_id):
        if github_authenticator.authentication():
            return User(user_id)
        return None

    login_manager.init_app(app)

    @app.route('/', methods=['POST'])
    @login_required
    @roles_required(Roles.WRITER)
    def add_title():
        app.logger.info("Attempting to add new item with title %s", request.form.get('title'))
        result = mongo_database.add_item(request.form.get('title'))
        app.logger.info("Inserted item with title: %s and id: %s", request.form.get('title'), result.inserted_id)
        return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():

        items = mongo_database.get_items()
        item_view_model = ViewModel(items)
        role_id = flask_login.current_user.role.value
        return render_template('index.html', view_model=item_view_model, role_id=role_id)

    @app.route('/complete_items/<id>')
    @login_required
    @roles_required(Roles.WRITER)
    def complete_items(id):
        app.logger.info("Completing item with id: %s", id)
        mongo_database.complete_item(id)
        return redirect(url_for('index'))

    @app.route('/move_todo/<id>')
    @login_required
    @roles_required(Roles.WRITER)
    def set_doing(id):
        app.logger.info("Move item to doing with id: %s", id)
        mongo_database.set_doing(id)
        return redirect(url_for('index'))

    @app.route('/undo_complete/<id>')
    @login_required
    @roles_required(Roles.WRITER)
    def undo_complete(id):
        app.logger.info("Undo completing item with id: %s", id)
        mongo_database.set_todo(id)
        return redirect(url_for('index'))


    @app.route('/create_board/<name>')
    @login_required
    @roles_required(Roles.WRITER)
    def create_board(name):
        mongo_database.create_board(name)
        return redirect(url_for('index'))

    @app.route('/login/callback', methods=["GET"])
    def github_authentication():
        user = github_authenticator.post_github_identity(request)
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return app

