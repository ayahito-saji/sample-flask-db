import os
from flask import Flask, render_template, g, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

if os.environ.get('DATABASE_URL') is not None:
    db_uri = os.environ.get('DATABASE_URL')
else:
    db_uri = "sqlite:///" + os.path.join(app.root_path, 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
db.init_app(app)

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', db_uri=db_uri)

@app.route('/entries')
def entries_index():
    entries = Entry.query.all()
    return render_template('entry/index.html', entries=entries)

@app.route('/entries/new', methods=["GET", "POST"])
def entries_new():
    if request.method == "GET":
        return render_template('entry/new.html')
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        print("title: " + title)
        print("body: " + body)

        entry = Entry()
        entry.title = title
        entry.body = body
        db.session.add(entry)
        db.session.commit()

        return redirect("/entries/"+str(entry.id))

@app.route('/entries/<id>')
def entries_show(id):
    entry = Entry.query.get(id)
    return render_template('entry/show.html', entry=entry)

@app.route('/entries/<id>/edit', methods=["GET", "POST"])
def entries_edit(id):
    entry = Entry.query.get(id)
    if request.method == "GET":
        return render_template('entry/edit.html', entry=entry)
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        print("title: " + title)
        print("body: " + body)

        entry.title = title
        entry.body = body
        db.session.add(entry)
        db.session.commit()

        return redirect("/entries/"+str(entry.id))

@app.route('/entries/<id>/delete', methods=["POST"])
def entries_delete(id):
    if request.form['_method'] == 'DELETE':
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
        return redirect("/entries")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)