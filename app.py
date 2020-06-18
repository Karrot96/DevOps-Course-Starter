from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from trello.helpers import Trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')
trello_board = Trello("6yxcx50y")


@app.route('/', methods=['POST'])
def add_title():
    session.add_item(request.form.get('title'))
    return redirect(url_for('index'))


@app.route('/')
def index():
    items = trello_board.get_items()
    return render_template('index.html', items=sorted(items, key=lambda item: item['status'], reverse=True))


@app.route('/update_items', methods=['POST'])
def update_items():
    for item in trello_board.get_items():
        item_completed = request.form.get(str(item['id']))
        if item_completed == "on":
            item['status'] = "Completed"
            session.save_item(item)
        if item_completed is None:
            item['status'] = "Not Started"
            session.save_item(item)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
