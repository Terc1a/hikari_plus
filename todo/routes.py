from flask import Flask, request, render_template, url_for, redirect, make_response, flash, session
from sqlalchemy import select
from todo.models import ToDo, db, Tag, News, Users
import datetime
import plotly.graph_objs as go
import plotly.io as pio
import plotly.utils
import json
from flask_ckeditor import CKEditor
import flask_login
from flask_login import current_user, login_user, login_required, UserMixin, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from todo.userlogin import UserLogin

ckeditor = CKEditor()
login_manager = flask_login.LoginManager()

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['VERSION_CHECK'] = False
    app.secret_key = 'a1dcbe59291f58c089qwer4feaf8ee8e2f44f05cdd4465e0d9c726938b2eeaab'
    db.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    return app

app = create_app()
@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(Users, int(user_id))
    return user

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template('todo/login.html')

#Главная страница
@app.get('/')
@login_required
def home():

    if current_user:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
        tags_ids = []
        for el in get_curr_user_tags:
            tags_ids.append(el.id)
        todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).order_by(ToDo.is_complete).order_by(ToDo.id.desc()).all()
        todo_completed = ToDo.query.filter_by(is_complete=1, id=current_user.id).order_by(ToDo.id.desc()).all()
        todo_uncompleted = ToDo.query.filter_by(is_complete=0, id=current_user.id).order_by(ToDo.id.desc()).all()
        completed = len(todo_completed)
        uncompleted = len(todo_uncompleted)
        all = len(todo_list)
        todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
        return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')
    else:
        return redirect(url_for('todo/login.html'))




#Cкрываем выполненные
@app.get('/uncompleted')
def uncompleted():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
    tags_ids = []
    for el in get_curr_user_tags:
        tags_ids.append(el.id)
    todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    todo_completed = ToDo.query.filter_by(is_complete=1, id=current_user.id).order_by(ToDo.id.desc()).all()
    todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    completed = len(todo_completed)
    all = len(todo_list)
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=todo_uncompleted, todo_all=all, title='CUBI Prot.')


@app.post('/add')
def add():
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    get_tag = Tag.query.filter_by(title=request.form.get('tags-list'), uid=current_user.id).first()
    tag_id = get_tag.id
    descr = request.form.get('ckeditor')
    new_todo = ToDo(title=title, descr=descr, tag_id=tag_id,create_date=timenow, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/sort/<string:todo_tag>')
def sort(todo_tag):
    get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
    tags_ids = []
    tags_ids = []
    for el in get_curr_user_tags:
        tags_ids.append(el.id)
    todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    todo_completed = ToDo.query.filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    completed = len(todo_completed)
    uncompleted = len(todo_uncompleted)
    all = len(todo_list)
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
    return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.')


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
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)

    return render_template('todo/modal.html', todo_list=one_todo, todo_tags=todo_tags)


@app.post('/change_content/<int:todo_id>')
def update_task(todo_id):
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.title = request.form.get('title')
    #todo.tag = request.form.get('tag')
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



#Cтатистика
@app.get('/task_stats')
def stats():
    #Сбор данных по выполненным задачам
    get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
    tags_ids = []
    tags_ids = []
    for el in get_curr_user_tags:
        tags_ids.append(el.id)
    todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    todo_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).all()
    todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
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
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
    for el in todo_tags:
        todo = ToDo.query.filter_by(tag_id=el.id).order_by(ToDo.is_complete).all()
        if todo:
            print(todo)
            tag.append(el.id)
       
        else:
            pass
    for i in tag:
        todo = ToDo.query.filter_by(tag_id=i).order_by(ToDo.is_complete).all()
        if todo:
            tag_counter.update({f'{i}':todo})
        else:
            pass
    for i in tag:
        elem_count.update({f'{i}': len(tag_counter.get(f'{i}'))})
        data2.append(go.Bar(x=[len(todo_list)], y=[elem_count.get(f'{i}')], name=f'{i}'))
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
    todo_tags = Tag.query.filter_by(uid=current_user.id).all()
    get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
    tags_ids = []
    for el in get_curr_user_tags:
        tags_ids.append(el.id)
    tasks_all = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
    tasks_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).all()

    list_sorted = []
    list_sorted2 = []
    dates = []
    dates2 = []
    counter = []

    if request.method == 'GET':
        data_list_created = []
        data_list_completed = []
        dates_created = []
        dates_completed = []
        counter = []
        #Для созданных задач
        for task in tasks_all:
            date = task.create_date.split(" ")[0]
            data_list_created.append({task.id:date})
        for el in data_list_created:
            for date in el.values():
                if type(date) == list:
                    dates_created += date
                else:
                    dates_created.append(date)
    #получаю уникальные значения дат и количество задач по ним
        dates_unique = set(dates_created)
        matches = [{a:dates_created.count(a)} for a in sorted(dates_unique)]
        fig3 = go.Figure()
        keys = []
        values = []
        for i in matches:
            key,value = list(i.items())[0]
            keys.append(key)
            values.append(value)
        counter.append(go.Scatter(x=keys, y=values, name=f'Создано'))

        #Для завершенных задач
        for task in tasks_completed:
            print(task, 'task')
            date = task.close_date.split(" ")[0]
            data_list_completed.append({task.id:date})
        for el in data_list_completed:
            for date in el.values():
                if type(date) == list:
                    dates_completed += date
                else:
                    dates_completed.append(date)
        dates_unique2 = set(dates_completed)
        matches2 = [{a:dates_completed.count(a)} for a in sorted(dates_completed)]
        keys2 = []
        values2 = []
        for i in matches2:
            key,value = list(i.items())[0]
            keys2.append(key)
            values2.append(value)
        counter.append(go.Scatter(x=keys2, y=values2, name=f'Завершено'))
            #Отрисовка графов    
        fig3.update_layout(legend_orientation="h",
            legend=dict(x=.5, xanchor="center"),
            title=f"Задачи по всем проектам",
            xaxis_title="Даты",
            yaxis_title="Количество задач в день",
            margin=dict(l=0, r=0, t=50, b=0), 
            template='plotly_dark',
            )

        for el in counter:

            fig3.add_trace(el)
        graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('todo/project_stats.html', todo_tags=todo_tags, graphJSON=graphJSON)
    
    #по дефолту выводить график для самого первого проекта из запроса, по нажатию кнопки выводить график по выбранному
    if request.method == 'POST':
        tagss = request.form.get('tags-list')
        todo_tags = Tag.query.filter_by(uid=current_user.id, title=tagss).all()
        get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
        tags_ids = []
        for el in get_curr_user_tags:
            tags_ids.append(el.id)
        #tasks_all = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
        tasks_on_tag = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).all()
        #Для графа с созданными задачами
        for task in tasks_on_tag:
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
        counter.append(go.Scatter(x=keys, y=values, name=f'Создано'))
        #Для графа с завершенными задачами
        tasks_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).all()
        for task in tasks_completed:
            print(task, 'task')
            date = task.close_date.split(" ")[0]
            list_sorted2.append({task.id:date})
        for el in list_sorted2:
            for date in el.values():
                if type(date) == list:
                    dates2 += date
                else:
                    dates2.append(date)
        dates_unique2 = set(dates2)
        matches2 = [{a:dates2.count(a)} for a in sorted(dates_unique2)]
        keys2 = []
        values2 = []
        for i in matches2:
            key,value = list(i.items())[0]
            keys2.append(key)
            values2.append(value)
        counter.append(go.Scatter(x=keys2, y=values2, name=f'Завершено'))

    fig3.update_layout(legend_orientation="h",
        legend=dict(x=.5, xanchor="center"),
        title=f"Задачи по проекту {tagss}",
        xaxis_title="Даты",
        yaxis_title="Количество задач в день",
        margin=dict(l=0, r=0, t=50, b=0), 
        template='plotly_dark',
        )
    for el in counter:

        fig3.add_trace(el)
    graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('todo/project_stats.html', todo_tags=todo_tags, graphJSON=graphJSON)



#Админка
@app.get('/admin')
def admin():
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
   #news_list = News.query.all()
    return render_template('todo/admin.html', tag_list=todo_tags)


@app.post('/add_tag')
def add_tag():
    title = request.form.get('title')
    descr = request.form.get('descr')
    uid = current_user.id
    new_tag = Tag(title=title, descr=descr, uid=uid)
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
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)

    return render_template('todo/modal2.html', todo_list=one_todo, todo_tags=todo_tags)

#поиск заметки по названию
@app.post('/search')
def search():
    get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
    tags_ids = []
    for el in get_curr_user_tags:
        tags_ids.append(el.id)
    search_bar = request.form.get('search_bar')
    search = "%{}%".format(search_bar)
    one_todo = ToDo.query.filter(ToDo.title.like(search), ToDo.tag_id.in_((tags_ids))).all()
    if not one_todo:
            one_todo = ToDo.query.filter(ToDo.descr.like(search), ToDo.tag_id.in_((tags_ids))).all()

    return render_template('todo/index.html', todo_list=one_todo)

@app.route('/settings')
def settings():
    return render_template('todo/settings.html')

@app.route('/change_theme', methods=['POST',  'GET'])
def article():
    if request.method == 'POST':
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('settings')
        return res, 302

    return render_template('todo/settings.html')


@app.route('/change_snow_state', methods=['POST',  'GET'])
def snow():
    if request.method == 'POST':
        res = make_response("")
        res.set_cookie("snow_state", request.form.get('snow_state'), 60*60*24*15)
        res.headers['location'] = url_for('settings')
        return res, 302

    return render_template('todo/settings.html')

@app.route('/release')
def release():
    news_list = News.query.all()

    return render_template('todo/about.html', news_list=news_list)

@app.post('/create_news')
def create_news():
    timed_raw = datetime.datetime.now()
    timed = (str(timed_raw)).rsplit('.', 2)
    timenow = timed[0]
    title = request.form.get('title')
    version = request.form.get('version')
    descr = request.form.get('ckeditor')
    to_send = False
    new_post = News(title=title, descr=descr, version=version,create_date=timenow, to_send=to_send)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('todo/login.html')
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form['name']).first()
        if user and check_password_hash(user.password, request.form['psw']):
            print(f'logged in by {user.id}') 
            user = User(user.id) 
            login_user(user)
            return redirect(url_for('home'))

        flash("Неверная пара логин/пароль", "error")
 
    # return render_template("todo/login.html", title="Авторизация")



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        timed_raw = datetime.datetime.now()
        timed = (str(timed_raw)).rsplit('.', 2)
        timenow = timed[0]
        if len(request.form.get('name')) > 4 and len(request.form.get('email')) > 4 \
        and len(request.form.get('psw')) >4 and request.form.get('psw') == request.form.get('psw2'):
            hash = generate_password_hash(request.form['psw'])
            check_usermail_exist = Users.query.filter_by(email=request.form.get('email')).all()
            check_username_exist = Users.query.filter_by(username=request.form.get('name')).all()
            if check_usermail_exist:
                flash('Пользователь с данной почтой уже существует')
            elif check_username_exist:
                flash('Пользователь с данным логином уже существует')
            else:
                add_user = Users(username=request.form.get('name'), email=request.form.get('email'), password=hash, register_date=timenow)
                db.session.add(add_user)
                db.session.commit()
                return redirect(url_for('home'))
        else:
            flash('Длина каждого поля не может быть меньше 4 символов')
            
    return render_template("todo/register.html", title="Регистрация")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))