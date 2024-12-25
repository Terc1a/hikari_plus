from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy import select
from todo.models import ToDo, db
import datetime
import plotly.graph_objs as go
import plotly.io as pio
import plotly.utils
import json


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()


@app.get('/')
def home():
<<<<<<< HEAD
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter_by(is_complete=0).all()
    completed = len(todo_completed)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')
=======
    # return 'Hello, Flask'
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, title='CUBI Prot.')
>>>>>>> 6a5e3f32d37e1a68168baff77762be8c833aaa2c

@app.post('/add')
def add():
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    tag = request.form.get('tag')
    descr = request.form.get('descr')
<<<<<<< HEAD
    new_todo = ToDo(title=title, descr=descr, tag=tag,create_date=timenow, is_complete=False)
=======
    new_todo = ToDo(title=title, descr=descr, tag=tag, is_complete=False)
>>>>>>> 6a5e3f32d37e1a68168baff77762be8c833aaa2c
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/sort/<string:todo_tag>')
def sort(todo_tag):
<<<<<<< HEAD
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo = ToDo.query.filter_by(tag=todo_tag).order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter(ToDo.is_complete.like('0')).filter(ToDo.tag.like(todo_tag)).all()
    completed = len(todo_completed)
    print(todo_uncompleted)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')
=======
    todo = ToDo.query.filter_by(tag=todo_tag).order_by(ToDo.is_complete).all()
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    return render_template('todo/index.html', todo_list=todo, todo_tags=todo_tags, title='CUBI Prot.')
>>>>>>> 6a5e3f32d37e1a68168baff77762be8c833aaa2c

@app.get('/update/<int:todo_id>')
def update(todo_id):
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.is_complete = not todo.is_complete
    todo.close_date = timenow
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update_content/<int:todo_id>', methods=['GET', 'POST'])
def update_content(todo_id):
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    tag = request.form.get('tag')
    descr = request.form.get('descr')
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.is_complete = todo.is_complete
    todo.create_date = timenow
    todo.title = title
    todo.tag = tag
    todo.descr = descr
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/change_content/<int:todo_id>')
def update_task(todo_id):
    todo_list = ToDo.query.filter_by(id=todo_id).order_by(ToDo.is_complete).all()
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    tag = request.form.get('tag')
    descr = request.form.get('descr')
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.is_complete = todo.is_complete
    todo.create_date = timenow
    todo.title = title
    todo.tag = tag
    todo.descr = descr
    db.session.commit()
    return render_template('todo/modal.html', todo_list=todo_list)


@app.get('/get_task')
def get_task(todo_id):
    pass


@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/create')
def create():
    return render_template('todo/new_task.html')


@app.get('/stats')
def stats():
    #Сбор данных по выполненным задачам
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=True).all()
    todo_uncompleted = ToDo.query.filter_by(is_complete=False).all()
    #Cбор данных по тегам
    tag = []
    tag_counter = {}
    elem_count = {}
    data2 = []
    todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    for el in todo_tags:
        tag.append(el.tag)
    for i in tag:
        todo = ToDo.query.filter_by(tag=i).order_by(ToDo.is_complete).all()
        
        tag_counter.update({f'{i}':todo})
    for i in tag:
        elem_count.update({f'{i}': len(tag_counter.get(i))})
        data2.append(go.Bar(x=[len(todo_list)], y=[elem_count.get(i)], name=f'{i}'))
    fig = go.Figure(data=[
        go.Bar(x=[len(todo_list)], y=[len(todo_list)], name='Все'),
        go.Bar( x=[len(todo_list)], y=[len(todo_completed)], name='Выполненные'),
        go.Bar( x=[len(todo_list)], y=[len(todo_uncompleted)], name='В работе'),     
    ])
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title="Статистика по задачам",
                  xaxis_title="Задачи по статусам",
                  yaxis_title="Всего задач",
                  margin=dict(l=0, r=0, t=50, b=0))
    fig2 = go.Figure(data2)
    fig2.update_layout(legend_orientation="h",
                legend=dict(x=.5, xanchor="center"),
                title="Количество задач по тегам",
                xaxis_title="Теги",
                yaxis_title="Задач с тегами",
                margin=dict(l=0, r=0, t=50, b=0))


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('todo/stats.html', graphJSON=graphJSON, graphJSON2=graphJSON2)


