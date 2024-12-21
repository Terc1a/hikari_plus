from flask import Flask, request, render_template, url_for, redirect
from todo.models import ToDo, db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()


@app.get('/')
def home():
    # return 'Hello, Flask'
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, title='CUBI Prot.')

@app.post('/add')
def add():
    title = request.form.get('title')
    tag = request.form.get('tag')
    descr = request.form.get('descr')
    new_todo = ToDo(title=title, descr=descr, tag=tag, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/sort/<string:todo_tag>')
def sort(todo_tag):
    todo = ToDo.query.filter_by(tag=todo_tag).order_by(ToDo.is_complete).all()
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo, todo_tags=todo_tags, title='CUBI Prot.')

@app.get('/update/<int:todo_id>')
def update(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.is_complete = not todo.is_complete
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))