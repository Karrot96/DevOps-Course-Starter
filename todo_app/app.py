from flask import Flask, render_template, request, redirect, url_for
import os
from todo_app.trello.trello_api import TrelloAPI
from todo_app.models.view_model import ViewModel


def create_app():
    app = Flask(__name__)
    trello_board = TrelloAPI(os.environ['TRELLO_BOARD_ID'])

    @app.route('/', methods=['POST'])
    def add_title():
        trello_board.add_item(request.form.get('title'))
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        items = trello_board.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/complete_items/<id>')
    def complete_items(id):
        trello_board.complete_item(id)
        return redirect(url_for('index'))


    @app.route('/move_todo/<id>')
    def set_doing(id):
        trello_board.set_doing(id)
        return redirect(url_for('index'))

    @app.route('/undo_complete/<id>')
    def undo_complete(id):
        trello_board.set_todo(id)
        return redirect(url_for('index'))

    @app.route('/create_board/<name>')
    def create_board(name):
        trello_board.create_board(name)
        return redirect(url_for('index'))

    return app

