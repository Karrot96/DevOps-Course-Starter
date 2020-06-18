from flask import Flask, render_template, request, redirect, url_for
from trello.helpers import Trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')
trello_board = Trello("6yxcx50y")


@app.route('/', methods=['POST'])
def add_title():
    trello_board.add_item(request.form.get('title'))
    return redirect(url_for('index'))


@app.route('/')
def index():
    items = [
        {
            **item,
            **{"url": f"{url_for('complete_items',id=item['id'])}"}
        } for item in trello_board.get_items() if item["status"] == "Not Started"
    ]
    items += [
        {
            **item,
            **{"url": f"{url_for('undo_complete',id=item['id'])}"}
        } for item in trello_board.get_items() if item["status"] == "Completed"
    ]
    return render_template('index.html', items=sorted(items, key=lambda item: item['status'], reverse=True))


@app.route('/update_items', methods=['POST'])
def update_items():
    for item in trello_board.get_items():
        item_completed = request.form.get(str(item['id']))
        if item_completed == "on":
            trello_board.complete_item(item["id"])
    return redirect(url_for('index'))

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
