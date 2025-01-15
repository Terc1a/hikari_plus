from flask import Flask, request, render_template, url_for, redirect, make_response, flash, session, send_from_directory
from sqlalchemy import select
from todo.models import ToDo, db, Tag, News, Users
from datetime import datetime
from time import gmtime, strftime
import plotly.graph_objs as go
import plotly.io as pio
import plotly.utils
import json
import pytz
from flask_ckeditor import CKEditor
import flask_login
from flask_login import current_user, login_user, login_required, UserMixin, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

ckeditor = CKEditor()
login_manager = flask_login.LoginManager()
UPLOAD_FOLDER = '/path/to/the/uploads'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'mp4'}
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['VERSION_CHECK'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

class timedt:
    timed = datetime.now()        
    GMT = pytz.timezone("Etc/GMT")
    dt = GMT.localize(timed)
    dt = timed.astimezone(GMT)
    def time_checker(self):
        return self.timed, self.dt
         

#Главная страница
@app.route('/', methods=['POST', 'GET'])
@login_required

def home():
    if request.method == 'GET':
        if current_user:
            #Смотреть дату в timed_raw и в gmt-0, и если timed_raw < gmt && gmt >= 5AM, то is_complete=0 where is_cycle=checked
            print(timedt().timed)
            timed_raw = timedt().timed
            dt_gmt = timedt().dt
            get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
            tags_ids = []
            default_value = 0
            for el in get_curr_user_tags:
                tags_ids.append(el.id)
            #Откат цикличных задач(в 00 GMT или же 03 MSC)
            cycle = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_cycle='checked').order_by(ToDo.id.desc()).all()
            for task in cycle:
                el = task.create_date
                el2 = task.close_date
                if el.month > dt_gmt.month and el.day > dt_gmt.day:
                    if el.day >= dt_gmt.day and dt_gmt.hour >= 0:
                            print(task.title, '1')
                            task.is_complete = not task.is_complete
                            task.create_date = timed_raw
                            task.close_date = datetime(9999, 12, 31, 00, 00, 00, 000000)
                            db.session.commit()
                elif el.month == dt_gmt.month and el.day < dt_gmt.day and dt_gmt.hour >= 0:
                    for task in cycle:
                        print(task.title, '2')
                        task.is_complete = not task.is_complete
                        task.create_date = timed_raw
                        task.close_date = datetime(9999, 12, 31, 00, 00, 00, 000000)
                        db.session.commit()            
                else:
                    if el.day < dt_gmt.day and dt_gmt.hour >= 0:
                        for task in cycle:
                            print(task.title, '3')
                            task.is_complete = not task.is_complete
                            task.create_date = timed_raw
                            task.close_date = datetime(9999, 12, 31, 00, 00, 00, 000000)
                            db.session.commit()
                delta = (timed_raw - task.close_date).days
                if delta == 0:
                    pass
                else:
                    task.cycle_series = 0
                    db.session.commit()
            #Рендер списков задач                   
            todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).order_by(ToDo.is_complete).order_by(ToDo.id.desc()).all()
            todo_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).order_by(ToDo.id.desc()).all()
            todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
            completed = len(todo_completed)
            uncompleted = len(todo_uncompleted)
            all = len(todo_list)
            todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
            return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.', default_value=default_value)
        else:
            return redirect(url_for('todo/login.html'))
    if request.method == 'POST':
        if current_user:
            check_flag = request.form.get('hider')
            if check_flag == '1':
                return redirect(url_for('home'))    
            else:
                get_curr_user_tags = Tag.query.filter_by(uid=current_user.id).all()
                tags_ids = []
                for el in get_curr_user_tags:
                    tags_ids.append(el.id)
                todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
                todo_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).order_by(ToDo.id.desc()).all()
                todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
                completed = len(todo_completed)
                uncompleted = len(todo_uncompleted)
                default_value = 1
                all = len(todo_list)
                todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
                return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all,  title='CUBI Prot.', default_value=default_value)
        else:
            return redirect(url_for('todo/login.html'))


#Создаем пост
@app.post('/add')
@login_required
def add():
    timed_raw = timedt().timed
    title = request.form.get('title')
    is_cycle = request.form.get('checker')
    get_tag = Tag.query.filter_by(title=request.form.get('tags-list'), uid=current_user.id).first()
    tag_id = get_tag.id
    descr = request.form.get('ckeditor')
    if is_cycle == None:
        new_todo = ToDo(title=title, descr=descr, tag_id=tag_id,create_date=timed_raw, is_complete=False)
        db.session.add(new_todo)
        db.session.commit()
    else:
        cycle_series = 0
        new_todo = ToDo(title=title, descr=descr, tag_id=tag_id,create_date=timed_raw, is_complete=False, is_cycle=is_cycle, cycle_series=cycle_series)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('home'))


#Сортируем по проектам
@app.route('/sort/<string:todo_tag>', methods=['POST', 'GET'])
@login_required
def sort(todo_tag):
    if request.method == 'GET':
        default_value = 0
        get_curr_user_tags = Tag.query.filter_by(uid=current_user.id, title=todo_tag).all()
        tags_ids = []
        tags_ids = []
        for el in get_curr_user_tags:
            tags_ids.append(el.id)
        todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).order_by(ToDo.is_complete).order_by(ToDo.id.desc()).all()
        todo_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).all()
        todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
        todo_list_all = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).all()
        completed = len(todo_completed)
        uncompleted = len(todo_uncompleted)
        all = len(todo_list_all)
        todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
        return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all, title='CUBI Prot.', default_value=default_value)
    if request.method == 'POST':
        if current_user:
            check_flag = request.form.get('hider')
            if check_flag == '1':
                return redirect(url_for('home'))    
            else:
                get_curr_user_tags = Tag.query.filter_by(uid=current_user.id, title=todo_tag).all()
                tags_ids = []
                for el in get_curr_user_tags:
                    tags_ids.append(el.id)
                todo_list = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
                todo_completed = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=1).order_by(ToDo.id.desc()).all()
                todo_uncompleted = ToDo.query.filter(ToDo.tag_id.in_((tags_ids))).filter_by(is_complete=0).order_by(ToDo.id.desc()).all()
                completed = len(todo_completed)
                uncompleted = len(todo_uncompleted)
                default_value = 1
                all = len(todo_list)
                todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
                return render_template('todo/index.html', todo_list=todo_list, todo_tags=todo_tags, todo_completed=completed, todo_uncompleted=uncompleted, todo_all=all,  title='CUBI Prot.', default_value=default_value)
        else:        
            return redirect(url_for('todo/login.html'))

#Изменяем статус задачи
@app.get('/update/<int:todo_id>')
@login_required
def update(todo_id):
    timed_raw = timedt().timed
    todo = ToDo.query.filter_by(id=todo_id).first()
    title_change = todo.title
    todo.title = title_change[3:-4]
    todo.is_complete = not todo.is_complete
    todo.close_date = timed_raw
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/finish/<int:todo_id>')
@login_required
def finish(todo_id):
    timed_raw = timedt().timed
    todo = ToDo.query.filter_by(id=todo_id).first()
    some = todo.title
    if "</" in some:
        pass
    else:
        todo.title = f'<s>{some}</s>'
    test = todo.is_cycle
    if todo.is_cycle=='checked':
        todo.cycle_series +=1
        
    todo.is_complete = 1
    todo.close_date = timed_raw
    db.session.commit()
    return redirect(url_for('home'))    

#Получаем задачу
@app.get('/get_task/<int:todo_id>')
@login_required
def get_task(todo_id):
    one_todo = ToDo.query.filter_by(id=todo_id).all()
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)

    return render_template('todo/modal.html', todo_list=one_todo, todo_tags=todo_tags)


#Изменяем задачу
@app.post('/change_content/<int:todo_id>')
@login_required
def update_task(todo_id):
    timed_raw = timedt().timed
    todo = ToDo.query.filter_by(id=todo_id).first()
    todo.title = request.form.get('title')
    #todo.tag = request.form.get('tags-list')
    todo.descr = request.form.get('ckeditor')
    todo.create_date = timed_raw
    db.session.commit()
    return redirect(url_for('home'))


#Удаляем задачу
@app.get('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))



#Cтатистика
@app.get('/task_stats')
@login_required
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
            dt = str(el.create_date).split(' ')
            data3.append(dt[0])

    for date in data3:
        if date not in uniq_date:
            uniq_date.append(date)
    #todo_tags = ToDo.query.distinct(ToDo.tag).group_by(ToDo.tag)
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
    for el in todo_tags:
        todo = ToDo.query.filter_by(tag_id=el.id).order_by(ToDo.is_complete).all()
        if todo:
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


#Статистика по проектам
@app.route('/project_stats', methods=['POST', 'GET'])
@login_required
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
            date = str(task.create_date).split(" ")[0]
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
            date = str(task.close_date).split(" ")[0]
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
            date = str(task.create_date).split(" ")[0]
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
            date = str(task.close_date).split(" ")[0]
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
@login_required
def admin():
    if current_user.id !=1:
        todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
        return render_template('todo/admin.html', tag_list=todo_tags)
    else:
        news_list = News.query.all()
        todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)
        return render_template('todo/admin.html', tag_list=todo_tags, news_list=news_list)



#Добавляем проект
@app.post('/add_tag')
@login_required
def add_tag():
    title = request.form.get('title')
    descr = request.form.get('descr')
    uid = current_user.id
    check_tag_exist = Tag.query.filter_by(uid=uid).filter_by(title=title).all()
    if not check_tag_exist:
        new_tag = Tag(title=title, descr=descr, uid=uid)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        flash_msg = 'Проект с таким названием уже существует, выберите другое название'
        flash(flash_msg)
        return redirect('http://192.168.0.17:5555/admin#openModal')


#Получаем проект
@app.get('/get_tag/<int:tag_id>')
@login_required
def get_tag(tag_id):
    one_tag = Tag.query.filter_by(id=tag_id).all()
    return render_template('todo/tag_modal.html', tag_list=one_tag)


#Изменяем проект
@app.post('/change_tag/<int:tag_id>')
@login_required
def change_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    tag.title = request.form.get('title')
    tag.descr = request.form.get('descr')
    db.session.commit()
    return redirect(url_for('admin'))


#Удаляем проект
@app.get('/delete_tag/<int:tag_id>')
@login_required
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('admin'))


#Получаем полное описание задачи
@app.get('/get_detail/<int:todo_id>')
@login_required
def get_detail(todo_id):
    one_todo = ToDo.query.filter_by(id=todo_id).all()
    todo_tags = Tag.query.filter_by(uid=current_user.id).distinct(Tag.title)

    return render_template('todo/modal2.html', todo_list=one_todo, todo_tags=todo_tags)


#поиск заметки по названию
@app.post('/search')
@login_required
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


#Открываем страницу настроек
@app.route('/settings')
@login_required
def settings():
    return render_template('todo/settings.html')


#Изменяем тему приложения
@app.route('/change_theme', methods=['POST',  'GET'])
@login_required
def article():
    if request.method == 'POST':
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('settings')
        return res, 302

    return render_template('todo/settings.html')


#Изменяем эффекты на заднем фоне
@app.route('/change_snow_state', methods=['POST',  'GET'])
@login_required
def snow():
    if request.method == 'POST':
        res = make_response("")
        res.set_cookie("snow_state", request.form.get('snow_state'), 60*60*24*15)
        res.headers['location'] = url_for('settings')
        return res, 302

    return render_template('todo/settings.html')


#Переходим на страницу новостей
@app.route('/release')
def release():
    news_list = News.query.all()

    return render_template('todo/about.html', news_list=news_list)


#Cоздаем новость
@app.post('/create_news')
@login_required
def create_news():
    timed_raw = timedt().timed
    title = request.form.get('title')
    version = request.form.get('version')
    descr = request.form.get('ckeditor')
    to_send = False
    new_post = News(title=title, descr=descr, version=version,create_date=timed_raw, to_send=to_send)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('admin'))


#Авторизуемся
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('todo/login.html')
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form['name']).first()
        if user and check_password_hash(user.password, request.form['psw']):
            session['username'] = request.form['name'] 
            user = User(user.id) 
            login_user(user)
            return redirect(url_for('home'))

        flash("Неверная пара логин/пароль", "error")
 

#Регистрируемся
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        timed_raw = timedt().timed

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
                add_user = Users(username=request.form.get('name'), email=request.form.get('email'), password=hash, register_date=timed_raw)
                tag_title = 'CUBI'
                tag_descr = 'Ознакомительный проект, который поможет освоиться в системе'
                task_title = 'Ознакомиться с системой'
                task_descr = 'Бла-бла-бла'
                db.session.add(add_user)
                db.session.commit()
                get_uid = Users.query.filter_by(username=request.form.get('name')).first()
                add_tag = Tag(uid=get_uid.id,title=tag_title, descr=tag_descr)
                db.session.add(add_tag)
                db.session.commit()
                get_tag = Tag.query.filter_by(uid=get_uid.id).filter_by(title=tag_title).first()
                add_task = ToDo(title=task_title, descr=task_descr, tag_id=get_tag.id,create_date=timed_raw, is_complete=False)
                db.session.add(add_task)
                db.session.commit()


                
                return redirect(url_for('home'))
        else:
            flash('Длина каждого поля не может быть меньше 4 символов')
            
    return render_template("todo/register.html", title="Регистрация")


#Выходим из системы
@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('login'))


#Рендерим страницу с гайдами
@app.route('/guides')
def guides():
    return render_template('todo/guides.html', title='Гайды')


#Загрузка файлов - пока неактуально
#Проверяем, что файл имеет подходящее расширение
def allowed_ext(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Загружаем файл на сервер
@app.post('/upload_video')
@login_required
def upload(filename):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не может быть загружен')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
        if file and allowed_ext(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Загрузить новый файл</title>
    <h1>Загрузить новый файл</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

