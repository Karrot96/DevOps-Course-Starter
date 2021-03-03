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
    app.config["SECRET_KEY"]=os.environ["SECRET_KEY"]
    mongo_database = MongoWrapper(os.environ['DEFAULT_DATABASE'])
    login_manager = LoginManager()
    github_authenticator = GithubAuthentication()

    @login_manager.unauthorized_handler
    def unauthenticated():
        authentication_url = github_authenticator.get_github_identity()
        return redirect(authentication_url)
        
    
    @login_manager.user_loader
    def load_user(user_id):
        if github_authenticator.authentication():
            print(user_id)
            return User(user_id)
        return None

    login_manager.init_app(app)

    @app.route('/', methods=['POST'])
    @login_required
    def add_title():
        if flask_login.current_user.check_role(Roles.WRITER):
            mongo_database.add_item(request.form.get('title'))
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
    def complete_items(id):
        if flask_login.current_user.check_role(Roles.WRITER):
            mongo_database.complete_item(id)
        return redirect(url_for('index'))
        


    @app.route('/move_todo/<id>')
    @login_required
    def set_doing(id):
        if flask_login.current_user.check_role(Roles.WRITER):
            mongo_database.set_doing(id)
        return redirect(url_for('index'))

    @app.route('/undo_complete/<id>')
    @login_required
    def undo_complete(id):
        if flask_login.current_user.check_role(Roles.WRITER):
            mongo_database.set_todo(id)
        return redirect(url_for('index'))

    @app.route('/create_board/<name>')
    @login_required
    def create_board(name):
        if flask_login.current_user.check_role(Roles.WRITER):
            mongo_database.create_board(name)
        return redirect(url_for('index'))

    @app.route('/login/callback', methods=["GET"])
    def github_authentication():
        user = github_authenticator.post_github_identity(request)
        flask_login.login_user(user)
        return redirect(url_for('index'))

    return app

