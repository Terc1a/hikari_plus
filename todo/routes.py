from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy import select
from todo.models import ToDo, db, Tag
import datetime
import plotly.graph_objs as go
import plotly.io as pio
import plotly.utils
import json
from flask_ckeditor import CKEditor

ckeditor = CKEditor()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['VERSION_CHECK'] = False
    db.init_app(app)
    ckeditor.init_app(app)
    return app

app = create_app()


#Главная страница
@app.get('/')
def home():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter_by(is_complete=0).all()
    completed = len(todo_completed)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = Tag.query.distinct(Tag.title)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')

#Cкрываем выполненные
@app.get('/uncompleted')
def uncompleted():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter_by(is_complete=0).all()
    completed = len(todo_completed)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = Tag.query.distinct(Tag.title)
    for el in todo_tags:
        print(el.title)
    return render_template('todo/index.html', todo_list=todo_uncompleted, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')


@app.post('/add')
def add():
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    tag = request.form.get('tags-list')
    descr = request.form.get('ckeditor')
    new_todo = ToDo(title=title, descr=descr, tag=tag,create_date=timenow, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/sort/<string:todo_tag>')
def sort(todo_tag):
    todo_list = ToDo.query.order_by(ToDo.is_complete).all()
    todo = ToDo.query.filter_by(tag=todo_tag).order_by(ToDo.is_complete).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter(ToDo.is_complete.like('0')).filter(ToDo.tag.like(todo_tag)).all()
    completed = len(todo_completed)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = Tag.query.distinct(Tag.title)
    return render_template('todo/index.html', todo_list=todo, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')


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


@app.get('/get_task/<int:todo_id>')
def get_task(todo_id):
    one_todo = ToDo.query.filter_by(id=todo_id).all()
    todo_tags = Tag.query.distinct(Tag.title)

    return render_template('todo/modal.html', todo_list=one_todo, todo_tags=todo_tags)


@app.post('/change_content/<int:todo_id>')
def update_task(todo_id):
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.title = request.form.get('title')
    todo.tag = request.form.get('tag')
    todo.descr = request.form.get('ckeditor')
    todo.create_date = timed[0]
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/create')
def create():
    return render_template('todo/new_task.html')


#Cтатистика
@app.get('/task_stats')
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
    data3 = []
    data4 = []
    uniq_date = []
    counter = []
    some_date = []

    for el in todo_list:
        if el.create_date is None:
            pass
        else:
            dt = el.create_date.split(' ')
            data3.append(dt[0])

    for date in data3:
        if date not in uniq_date:
            uniq_date.append(date)
    #todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    todo_tags = Tag.query.distinct(Tag.title)
    for el in todo_tags:
        tag.append(el.title)
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
                  margin=dict(l=0, r=0, t=50, b=0), template='plotly_dark')
    fig2 = go.Figure(data2)
    fig2.update_layout(legend_orientation="h",
                legend=dict(x=.5, xanchor="center"),
                title="Количество задач по тегам",
                xaxis_title="Задачи по тегам",
                yaxis_title="Задач с тегами",
                margin=dict(l=0, r=0, t=50, b=0), template='plotly_dark')
    
    #Добавить 3 график, совмещающий в себе 2 других
    fig3 = go.Figure()
    for i in tag:
        data4.append(go.Bar(x=[len(todo_list)], y=[elem_count.get(i)], name=f'{i}'))
    for i in data4:
        fig3.add_trace(i)
    for i in elem_count:
        some_date.append(elem_count.get(i))
    fig3.add_trace(go.Scatter(
    #количество задач по тегам разделено по дням
    x= [len(todo_list)],#задач по тегам было создано
    y= some_date,#задач по тегам было сделано
    ))
    for el in elem_count:
        counter.append(go.Scatter(x=[len(todo_list)], y=[elem_count.get(el)], name=f'{el}'))
    #fig3.add_trace(counter)


    fig3.update_layout(legend_orientation="h",
                legend=dict(x=.5, xanchor="center"),
                title="Количество задач по тегам",
                xaxis_title="Теги",
                yaxis_title="Задач с тегами",
                margin=dict(l=0, r=0, t=50, b=0), 
                template='plotly_dark',
                )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('todo/stats.html', graphJSON=graphJSON, graphJSON2=graphJSON2)

@app.route('/project_stats', methods=['POST', 'GET'])
def project_stats():
    todo_tags = Tag.query.distinct(Tag.title)
    list_sorted = []
    dates = []
    fig_create = []
    if request.method == 'GET':

        return render_template('todo/project_stats.html', todo_tags=todo_tags)
    #по дефолту выводить график для самого первого проекта из запроса, по нажатию кнопки выводить график по выбранному
    if request.method == 'POST':
        tagss = request.form.get('tags-list')
        todo_completed = ToDo.query.filter_by(tag=tagss).all()
        for task in todo_completed:
            date = task.create_date.split(" ")[0]
            list_sorted.append({task.id:date})
        for el in list_sorted:
            for date in el.values():
                if type(date) == list:
                    dates += date
                else:
                    dates.append(date)
    #получаю уникальные значения дат и количество задач по ним
        dates_unique = set(dates)
        matches = [{a:dates.count(a)} for a in sorted(dates_unique)]
        fig3 = go.Figure()
        keys = []
        values = []
        for i in matches:
            key,value = list(i.items())[0]
            keys.append(key)
            values.append(value)
        fig_create = go.Scatter(x=keys, y=values, name=f'{tagss}')
        fig3.add_trace(fig_create)
        fig3.update_layout(legend_orientation="h",
            legend=dict(x=.5, xanchor="center"),
            title=f"Задачи по проекту {tagss}",
            xaxis_title="Даты",
            yaxis_title="Количество задач в день",
            margin=dict(l=0, r=0, t=50, b=0), 
            template='plotly_dark',
            )
        graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('todo/project_stats.html', todo_tags=todo_tags, graphJSON=graphJSON)



#Админка
@app.get('/admin')
def admin():
    tag_list = Tag.query.all()
    for el in tag_list:
        print(el.title)

    return render_template('todo/admin.html', tag_list=tag_list)


@app.post('/add_tag')
def add_tag():
    title = request.form.get('title')
    descr = request.form.get('descr')
    new_tag = Tag(title=title, descr=descr)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('admin'))

@app.get('/get_tag/<int:tag_id>')
def get_tag(tag_id):
    one_tag = Tag.query.filter_by(id=tag_id).all()
    return render_template('todo/tag_modal.html', tag_list=one_tag)

@app.post('/change_tag/<int:tag_id>')
def change_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    tag.title = request.form.get('title')
    tag.descr = request.form.get('descr')
    db.session.commit()
    return redirect(url_for('admin'))

@app.get('/delete_tag/<int:tag_id>')
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('admin'))

@app.get('/get_detail/<int:todo_id>')
def get_detail(todo_id):
    one_todo = ToDo.query.filter_by(id=todo_id).all()
    todo_tags = Tag.query.distinct(Tag.title)

    return render_template('todo/modal2.html', todo_list=one_todo, todo_tags=todo_tags)

#поиск заметки по названию
@app.post('/search')
def search():
    search_bar = request.form.get('search_bar')
    search = "%{}%".format(search_bar)
    one_todo = ToDo.query.filter(ToDo.title.like(search)).all()
    if not one_todo:
            one_todo = ToDo.query.filter(ToDo.descr.like(search)).all()

    return render_template('todo/index.html', todo_list=one_todo)

