from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/', methods=['POST'])
def add_title():
    session.add_item(request.form.get('title'))
    return redirect(url_for('index'))


@app.route('/')
def index():
    def status_sort(item):
        if item['status'] == "Not Started":
            return 1
        else:
            return 2
    items = session.get_items()
    return render_template('index.html', items=sorted(items, key=status_sort))


@app.route('/update_items', methods=['POST'])
def update_items():
    for item in session.get_items():
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
