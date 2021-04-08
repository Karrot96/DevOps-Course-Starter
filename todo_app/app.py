from todo_app.user.user import Roles, User
import flask_login
from todo_app.github.github_authentication import GithubAuthentication
from todo_app.mongo.mongo_wrapper import MongoWrapper
from flask import Flask, render_template, request, redirect, url_for
import os
from todo_app.models.view_model import ViewModel
from flask_login import LoginManager, login_required


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]=os.environ.get("SECRET_KEY")
    mongo_database = MongoWrapper(os.environ.get('DEFAULT_DATABASE'))
    login_manager = LoginManager()
    github_authenticator = GithubAuthentication()

    def check_writer(function):
        def wrapper():
            if flask_login.current_user.check_role(Roles.WRITER):
                function()
            return redirect(url_for('index'))
        return wrapper

    @login_manager.unauthorized_handler
    def unauthenticated():
        authentication_url = github_authenticator.get_github_auth_url()
        return redirect(authentication_url)
        
    
    @login_manager.user_loader
    def load_user(user_id):
        if github_authenticator.authentication():
            return User(user_id)
        return None

    login_manager.init_app(app)

    @check_writer
    @app.route('/', methods=['POST'])
    @login_required
    def add_title():
        mongo_database.add_item(request.form.get('title'))

    @app.route('/')
    @login_required
    def index():
        items = mongo_database.get_items()
        item_view_model = ViewModel(items)
        role_id = flask_login.current_user.role.value
        return render_template('index.html', view_model=item_view_model, role_id=role_id)

    @check_writer
    @app.route('/complete_items/<id>')
    @login_required
    def complete_items(id):
        mongo_database.complete_item(id)
        

    @check_writer
    @app.route('/move_todo/<id>')
    @login_required
    def set_doing(id):
        mongo_database.set_doing(id)

    @check_writer
    @app.route('/undo_complete/<id>')
    @login_required
    def undo_complete(id):
        mongo_database.set_todo(id)


    @check_writer
    @app.route('/create_board/<name>')
    @login_required
    def create_board(name):
        mongo_database.create_board(name)

    @app.route('/login/callback', methods=["GET"])
    def github_authentication():
        user = github_authenticator.post_github_identity(request)
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return app

