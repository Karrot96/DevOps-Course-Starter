from flask import Flask, render_template, request, redirect, url_for
from trello.trello_api import TrelloAPI
from config.settings import TRELLO_BOARD_ID
from Models.view_model import ViewModel

app = Flask(__name__)
trello_board = TrelloAPI(TRELLO_BOARD_ID)


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


@app.route('/undo_complete/<id>')
def undo_complete(id):
    trello_board.set_todo(id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
