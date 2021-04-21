from todo_app.mongo.mongo_wrapper import MongoWrapper
from flask import Flask, render_template, request, redirect, url_for
import os
from todo_app.models.view_model import ViewModel


def create_app(database: str = "DefaultDatabase"):
    app = Flask(__name__)
    mongo_database = MongoWrapper(os.environ.get('MONGO_URL'), database)


    @app.route('/', methods=['POST'])
    def add_title():
        mongo_database.add_item(request.form.get('title'))
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        items = mongo_database.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/complete_items/<id>')
    def complete_items(id):
        mongo_database.complete_item(id)
        return redirect(url_for('index'))


    @app.route('/move_todo/<id>')
    def set_doing(id):
        mongo_database.set_doing(id)
        return redirect(url_for('index'))

    @app.route('/undo_complete/<id>')
    def undo_complete(id):
        mongo_database.set_todo(id)
        return redirect(url_for('index'))

    @app.route('/create_board/<name>')
    def create_board(name):
        mongo_database.create_board(name)
        return redirect(url_for('index'))

    return app

