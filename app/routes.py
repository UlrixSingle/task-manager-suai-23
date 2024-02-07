from app.forms import RegistrationForm, LoginForm
from app.forms import TaskAddForm
from app.forms import CommentForm
from flask import request
from flask import render_template, redirect, flash, url_for
from app import app
import psycopg
from app.user import User
from app import login_manager
from flask_login import UserMixin
from flask_login import login_user, current_user
from flask_login import logout_user
from datetime import date

# Корневой тест
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        print("register (GET)")
    elif request.method == 'POST':
        print("register (POST)")
    else:
        print("register Unknown")
        
    if current_user.is_authenticated:
        return redirect(url_for('home', cur_user_id = current_user.id))
    else:
        return redirect(url_for('welcome'))

@login_manager.user_loader
def load_user(id):
    with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
        cur = con.cursor()
        login, password, name = cur.execute('SELECT login, password, nickname '
                                      'FROM "user" '
                                      'WHERE user_id = %s', (id,)).fetchone()
    return User(id, login, password, name)

'''
# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if form.validate_on_submit():
        with psycopg.connect(...) as con:
            res = cur.execute('SELECT id, login, password ' 
                              'FROM "user" '
                              'WHERE login = %s', (login_form.login.data,)).fetchone()
        if res is None or not check_password_hash(res[2], login_form.password.data):
            flash('Попытка входа неудачна', 'danger')
            return redirect(url_for('login'))
        id, login, password = res
        user = User(id, login, password)
        login_user(user, remember=login_form.remember_me.data)
        flash(f'Вы успешно вошли в систему, {current_user.login}', 'danger')
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=login_form)

@app.route('/admin_home', methods=['GET','POST'])
def get_admin_home():
    message = "Состояние неопределенно"
    admin_system_role_id = 1
    user_system_role_id = 2
    
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            admin_names = cur.execute(f'SELECT "nickname" FROM "user" WHERE system_role_id = %s;', [1]).fetchall()
            user_names = cur.execute(f'SELECT "nickname" FROM "user" WHERE system_role_id = %s;', [2]).fetchall()
            return render_template('home.html',
                                    system_role_id=1,
                                    system_role = 'Администратор',
                                    nickname='Penguin',
                                    admin_names=admin_names,
                                    user_names=user_names)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
'''

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            page_header="Создание новой учетной записи"
            
            home_view=1
            home_page=0
            
            cur_user_id=1
            
            reg_form = RegistrationForm()
            reg_form.names = [name[0] for name in cur.execute( f'SELECT "nickname" FROM "user";').fetchall()]
            reg_form.logins = [login[0] for login in cur.execute( f'SELECT "login" FROM "user";').fetchall()]
            
            reg_form.system_role.choices = cur.execute( f'SELECT * FROM system_role;').fetchall()
            
            if reg_form.validate_on_submit():
                # создать запись в базе данных
                return f'Регистрация {reg_form.nickname.data} успешна'
            
            for fieldName, errorMessages in reg_form.errors.items():
                for err in errorMessages:
                    print(err)
                    
            return render_template( 'registration.html', 
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    cur_user_id=cur_user_id,
                                    title='Регистрация', 
                                    form=reg_form)

    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

# Ошибка
@app.route('/err', methods=['GET'])
def err():
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            page_header=""
            
            home_view=1
            home_page=0
            
        return render_template('err.html',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                cur_user_id=cur_user_id)
    
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

# Приветствующая страница
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    #try:
        page_header="Веб-приложение управления проектами"
                
        home_view=1
        if not current_user.is_authenticated:
            home_view=0
        
        home_page=0
        
        login_form = LoginForm()
        if login_form.validate_on_submit():
            res = None
            with psycopg.connect(host=app.config['DB_SERVER'], 
                                port=app.config['DB_PORT'],
                                user=app.config['DB_USER'], 
                                password=app.config['DB_PASSWORD'],
                                dbname=app.config['DB_NAME'],
                                connect_timeout=app.config['DB_TIMEOUT']) as con:
                cur = con.cursor()
                
                res = cur.execute('SELECT user_id, login, password, nickname ' 
                                        'FROM "user" '
                                        'WHERE login = %s', (login_form.login.data,)).fetchone()
                print(res)
                # if res is None or not check_password_hash(res[2], login_form.password.data):
                if res is None or not res[2] == login_form.password.data:
                    flash('Попытка входа неудачна', 'danger')
                    return redirect(url_for('welcome'))
                
                id, login, password, name = res
                user = User(id, login, password, name)
                login_user(user, remember=login_form.remember_me.data)
                flash(f'Вы успешно вошли в систему под логином {login}', 'danger')
                return redirect(url_for('home', cur_user_id=id)) 
          
        cur_user_id = None
        if current_user.is_authenticated:
            cur_user_id = current_user.id
        
        return render_template('welcome.html',
                                title='Вход',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                form=login_form,
                                current_user=current_user,
                                cur_user_id=cur_user_id)
    
    #except Exception as e:
    #    message = f"Ошибка подключения: {e}"
    #    return message
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))    

# Главная страница
@app.route('/<int:cur_user_id>/home', methods=['GET','POST'])
def home( cur_user_id):
    #try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('home', cur_user_id=current_user.id))
            
            page_header=""
            
            home_view=1   
            home_page=1
            system_role_admin_id = 1
            system_role_user_id = 2
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            
            admins = []
            users = []
            projects = []
            if system_role_id == system_role_admin_id:
                admins = cur.execute(f'SELECT "user_id", "nickname" FROM "user" WHERE system_role_id = %s;', [system_role_admin_id]).fetchall()
                users = cur.execute(f'SELECT "user_id", "nickname" FROM "user" WHERE system_role_id = %s;', [system_role_user_id] ).fetchall()
                projects = cur.execute(f'SELECT "project_id", "name" FROM "project"').fetchall()
            elif system_role_id == system_role_user_id:
                cur.execute(f'create table "prlist" as select "project_id", "role"."name" as "role_name", "job" from "role" join (select * from "team" where "user_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";', [cur_user_id])
                projects = cur.execute(f'select "project"."project_id" as "project_id", "project"."name" as "project_name", "role_name", "job" from "project" join "prlist" on "project"."project_id" = "prlist"."project_id";').fetchall()
                cur.execute(f'drop table "prlist";')
                
            cur_user_id = cur_user[3]
            
            page_header = str(system_role + " " + nickname)
            
            return render_template('home.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    system_role_id=system_role_id,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    admins=admins,
                                    users=users,
                                    projects=projects,
                                    system_role_admin_id=system_role_admin_id)
        
    #except Exception as e:
    #    message = f"Ошибка подключения: {e}"
    #    return message
    
@app.route('/<int:cur_user_id>/announce', methods=['GET','POST'])
def announce( cur_user_id):
    return 'OK'
    
@app.route('/<int:cur_user_id>/exit', methods=['GET','POST'])
def exit( cur_user_id):
    return 'OK'

@app.route('/<int:cur_user_id>/profile/<int:user_id>', methods=['GET','POST'])
def profile( cur_user_id, user_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('profile', cur_user_id=current_user.id, user_id=user_id))
            
            page_header=""
            
            home_view=1
            home_page=0
            system_role_admin_id = 1
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            user = cur.execute(
                f'SELECT "usr"."name", "usr"."nickname", "usr"."second_name", "usr"."first_name", "usr"."surname", "usr"."mail", "usr"."phone", "usr"."descr", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [user_id]).fetchone()
            
            access = 0
            if cur_user_id == user[8] or system_role_id == system_role_admin_id:
                access = 1
                
            if cur_user_id == user[8]:
                home_page=3
            
            page_header = str(system_role + " " + nickname)
            
            return render_template('profile.html',
                                   page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    user=user,
                                    access=access)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Доска задач проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/<string:sort_type>/<string:sort_way>', methods=['GET','POST'])
def project( cur_user_id, project_id, sort_type, sort_way):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project', cur_user_id=current_user.id, project_id=project_id, sort_type=sort_type, sort_way=sort_way))
            
            page_header=""
            
            home_view=1
            home_page=0
            project_page=1
            system_role_admin_id = 1
            owner_role_id = 1
            member_role_id = 2
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            stages=cur.execute( f'select * from "stage"').fetchall()
            
            tasks=[]
            tasks_n=[]
            for i in range(len(stages)):
                task_list = [cur.execute( f'select "task"."task_id", "task"."name" as "taskname", "descr", "begindate", "enddate", "stage_id", "task"."priority_id", "priority"."name" as "priority_name", "colour", "weight" from "task" join "priority" on "task"."priority_id" = "priority"."priority_id" where "task"."project_id" = %s and "task"."stage_id" = %s;', [project_id, i+1]).fetchall()]
                tasks += task_list
                tasks_n += [len(task_list[0])]
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
                [project_id])
            cur.execute( f'select "user"."user_id", "nickname", "role_name", "job" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
            prteam = cur.fetchall()
            
            pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
            cur.execute( f'drop table "prteam";')
            
            role_id = 0
            participent=0
            if not (pruser is None):
                role_id = pruser[0]
                participent=1
            
            pr_access_granted = 0
            if role_id == owner_role_id or role_id == member_role_id:
                pr_access_granted = 1
            
            page_header = str(system_role + " " + nickname)

            return render_template('project.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    system_role=system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    tasks=tasks,
                                    tasks_n=tasks_n,
                                    stages=stages,
                                    stages_length=len(stages),
                                    project=project,
                                    tasks_maxlength=max(tasks_n),
                                    access = pr_access_granted)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Доска задач проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/analise', methods=['GET','POST'])
def project_analise( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_analise', cur_user_id=current_user.id, project_id=project_id))
            
            page_header=""
            
            home_view=1
            home_page=0
            project_page=2
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            stages=[]
            tasks=[]
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            page_header = str(system_role + " " + nickname)

            return render_template('project_analise.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    system_role=system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    tasks=tasks,
                                    stages=stages,
                                    project=project)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message    

# Описание проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/descr', methods=['GET','POST'])
def project_descr( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_descr', cur_user_id=current_user.id, project_id=project_id))
            
            page_header= ""
            
            home_view=1
            home_page=0
            project_page=3
            system_role_admin_id = 1
            owner_role_id = 1
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
                [project_id])
            cur.execute( f'select "user"."user_id", "nickname", "role_name", "job" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
            prteam = cur.fetchall()
            
            pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
            cur.execute( f'drop table "prteam";')
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            page_header = str(system_role + " " + nickname)
            
            role_id = 0
            participent=0
            if not (pruser is None):
                role_id = pruser[0]
                participent=1
            
            pr_access_granted = 0
            if role_id == owner_role_id or system_role_id == system_role_admin_id:
                pr_access_granted = 1
            
            return render_template('project_descr.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project,
                                    team=prteam,
                                    participent=participent,
                                    access = pr_access_granted)

    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Выйти из проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/exit', methods=['GET','POST'])
def project_exit( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_exit', cur_user_id=current_user.id, project_id=project_id))
            
            cur.execute( f'delete from "team" where "user_id" = %s and "project_id" = %s', [cur_user_id, project_id]);
            return redirect(url_for('home', cur_user_id = cur_user_id) )
            
            '''
            page_header=""
            
            home_view=1
            home_page=0
            project_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            return render_template('project_exit.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project)
            '''
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Добавить участника в проект
@app.route('/<int:cur_user_id>/project/<int:project_id>/add_member', methods=['GET','POST'])
def project_user_add( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_user_add', cur_user_id=current_user.id))
            
            page_header=""
            
            home_view=1
            home_page=0
            project_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            return render_template('project_user_add.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Изменить настройки участника проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/edit_member/<user_id>', methods=['GET','POST'])
def project_user_edit( cur_user_id, user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_user_edit', cur_user_id=current_user.id, user_id=user_id, project_id=project_id))
            
            page_header=""
            
            home_view=1
            home_page=0
            project_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            return render_template('project_user_edit.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

# Удалить участника из проекта
@app.route('/<int:cur_user_id>/project/<int:project_id>/remove_member/<user_id>', methods=['GET','POST'])
def project_user_remove( cur_user_id, user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('project_user_remove', cur_user_id=current_user.id, user_id=user_id, project_id=project_id))
            
            cur.execute( f'delete from "team" where "user_id" = %s and "project_id" = %s', [user_id, project_id]);
            return redirect(url_for('project_descr', cur_user_id = cur_user_id, project_id = project_id) )
            
            '''
            page_header=""
            
            home_view=1
            home_page=0
            project_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            return render_template('project_exit.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project)
            '''
            
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

# Описание задачи
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<int:task_id>', methods=['GET','POST'])
def task( cur_user_id, project_id, task_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('task', cur_user_id=current_user.id, project_id=project_id, task_id=task_id))
            
            page_header= ""
            
            home_view=1
            home_page=0
            project_page=0
            system_role_admin_id = 1
            owner_role_id = 1
            
            project = cur.execute( f'select "project_id", "name" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur.execute( f'create table "task_stage" as select "task_id", "project_id", "task"."name" as "task_name", "descr", "begindate", "enddate", "stage"."name" as "stage_name", "priority_id", "type", "field", "user_id" from "task" join "stage" on "task"."stage_id" = "stage"."stage_id" where "task_id" = %s;', [task_id])
            task = cur.execute( 'select "task_id", "project_id", "task_name", "descr", "begindate", "enddate", "stage_name", "priority"."name" as "priority_name", "type", "field", "user_id" from "task_stage" join "priority" on "task_stage"."priority_id" = "priority"."priority_id";').fetchone();
            cur.execute( 'drop table "task_stage"');
            
            user_name = cur.execute( f'select nickname from "user" where "user_id" = %s', [task[10]]).fetchone();
            
            comments = cur.execute( f'select "comment_id", "postdate", "user"."nickname", "comment"."descr", "user"."user_id" from "comment" join "user" on "comment"."user_id" = "user"."user_id" where "comment"."task_id" = %s order by "comment"."comment_id";', [task_id]).fetchall()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            remove_access = 1
            edit_access = 1
            comment_access = 1
            
            page_header = str(system_role + " " + nickname)
            
            return render_template('task.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project,
                                    task=task,
                                    comments=comments,
                                    remove_access=remove_access,
                                    edit_access=edit_access,
                                    comment_access=comment_access,
                                    user_name=user_name)

    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Добавить в проект задачу
@app.route('/<int:cur_user_id>/project/<int:project_id>/newtask', methods=['GET','POST'])
def newtask( cur_user_id, project_id):
    with psycopg.connect(host=app.config['DB_SERVER'], 
                            port=app.config['DB_PORT'],
                            user=app.config['DB_USER'], 
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME'],
                            connect_timeout=app.config['DB_TIMEOUT']) as con:
        cur = con.cursor()
        
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        if not int(current_user.id) == cur_user_id:
            return redirect(url_for('newtask', cur_user_id=current_user.id, project_id=project_id))
        
        page_header= ""
        
        home_view=1     
        home_page=0
        project_page=3
        system_role_admin_id = 1
        owner_role_id = 1
        member_role_id = 2
        
        project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
        
        cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
            [project_id])
        cur.execute( f'select "user"."user_id", "nickname" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
        prteam = cur.fetchall()
        print(prteam)
        
        pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
        cur.execute( f'drop table "prteam";')
        
        cur_user = cur.execute(
            f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
            [cur_user_id]).fetchone()
        system_role_id = cur_user[0]
        system_role = cur_user[1]
        nickname = cur_user[2]
        cur_user_id = cur_user[3]
        
        page_header = str(system_role + " " + nickname)
        
        task_form = TaskAddForm()
        task_form.stage.choices = cur.execute( f'SELECT * FROM stage;').fetchall()
        task_form.priority.choices = cur.execute( f'SELECT "priority_id", "name" FROM priority;').fetchall()
        task_form.user.choices = prteam
        
        role_id = 0
        participent=0
        if not (pruser is None):
            role_id = pruser[0]
            participent=1
        
        pr_access_granted = 0
        if role_id == owner_role_id or role_id == member_role_id:
            pr_access_granted = 1
            
        if task_form.validate_on_submit():
            cur.execute( f'INSERT INTO "task" ("project_id", "name", "descr", "stage_id", "priority_id", "type", "field", "user_id") VALUES(%s, %s, %s, %s, %s, %s, %s, %s);', [project_id, task_form.name.data, task_form.descr.data, task_form.stage.data, task_form.priority.data, task_form.tasktype.data, task_form.taskfield.data, task_form.user.data])
            return redirect(url_for('project', cur_user_id = cur_user_id, project_id = project_id, sort_type = 'all', sort_way = 'none'))
                
        return render_template('newtask.html',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                project_page=project_page,
                                system_role = system_role,
                                nickname=nickname,
                                cur_user_id=cur_user_id,
                                project=project,
                                participent=participent,
                                access = pr_access_granted,
                                form=task_form)

# Редактировать задачу
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<int:task_id>/task_edit', methods=['GET','POST'])
def task_edit( cur_user_id, project_id, task_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('task_edit', cur_user_id=current_user.id, project_id=project_id, task_id=task_id))
            
            page_header=""
            
            home_view=1  
            home_page=0
            project_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            stages=[]
            tasks=[]
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            page_header = str(system_role + " " + nickname)

            return render_template('project_analise.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    project_page=project_page,
                                    system_role=system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    tasks=tasks,
                                    stages=stages,
                                    project=project)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message    
    
# Удалить задачу
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<int:task_id>/task_remove', methods=['GET','POST'])
def task_remove( cur_user_id, project_id, task_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            if not current_user.is_authenticated:
                return redirect(url_for('index'))
            if not int(current_user.id) == cur_user_id:
                return redirect(url_for('task_remove', cur_user_id=current_user.id, project_id=project_id, task_id=task_id))
            
            '''
            page_header=""
            
            home_view=1
            home_page=0
            project_page=2
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            stages=[]
            tasks=[]
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            page_header = str(system_role + " " + nickname)
            '''
            
            cur.execute( f'delete from "task" where "task_id" = %s', [task_id]);

            return redirect(url_for('project', cur_user_id = cur_user_id, project_id = project_id,  sort_type = 'all', sort_way = 'none') ) 
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message    

# Добавить комментарий
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<task_id>/newcomment', methods=['GET','POST'])
def newcomment( cur_user_id, project_id, task_id):
    with psycopg.connect(host=app.config['DB_SERVER'], 
                            port=app.config['DB_PORT'],
                            user=app.config['DB_USER'], 
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME'],
                            connect_timeout=app.config['DB_TIMEOUT']) as con:
        cur = con.cursor()
        
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        if not int(current_user.id) == cur_user_id:
            return redirect(url_for('newcomment', cur_user_id=current_user.id, project_id=project_id))
        
        page_header= ""
        
        home_view=1     
        home_page=0
        project_page=0
        system_role_admin_id = 1
        owner_role_id = 1
        member_role_id = 2
        
        project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
        
        cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
            [project_id])
        cur.execute( f'select "user"."user_id", "nickname" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
        prteam = cur.fetchall()
        print(prteam)
        
        pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
        cur.execute( f'drop table "prteam";')
        
        cur_user = cur.execute(
            f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
            [cur_user_id]).fetchone()
        system_role_id = cur_user[0]
        system_role = cur_user[1]
        nickname = cur_user[2]
        cur_user_id = cur_user[3]
        
        page_header = str(system_role + " " + nickname)
        
        comment_form = CommentForm()
        
        role_id = 0
        participent=0
        if not (pruser is None):
            role_id = pruser[0]
            participent=1
        
        comment_access = 0
        if role_id == owner_role_id or role_id == member_role_id or system_role == system_role_admin_id:
            comment_access = 1
            
        current_date = str(date.today())
            
        if comment_form.validate_on_submit():
            cur.execute( f'INSERT INTO "comment" ("task_id", "user_id", "postdate", "descr") VALUES(%s, %s, %s, %s);', [task_id, cur_user_id, current_date, comment_form.descr.data])
            return redirect(url_for('task', cur_user_id = cur_user_id, project_id = project_id, task_id=task_id))
                
        return render_template('newcomment.html',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                project_page=project_page,
                                system_role = system_role,
                                nickname=nickname,
                                cur_user_id=cur_user_id,
                                project=project,
                                form=comment_form,
                                current_date=current_date,
                                title='Новый комментарий')
    
# Редактировать комментарий
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<task_id>/comment_edit/<comment_id>', methods=['GET','POST'])
def comment_edit( cur_user_id, project_id, task_id, comment_id):
    with psycopg.connect(host=app.config['DB_SERVER'], 
                            port=app.config['DB_PORT'],
                            user=app.config['DB_USER'], 
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME'],
                            connect_timeout=app.config['DB_TIMEOUT']) as con:
        cur = con.cursor()
        
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        if not int(current_user.id) == cur_user_id:
            return redirect(url_for('editcomment', cur_user_id=current_user.id, project_id=project_id))
        
        page_header= ""
        
        home_view=1     
        home_page=0
        project_page=0
        system_role_admin_id = 1
        owner_role_id = 1
        member_role_id = 2
        
        project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
        
        cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
            [project_id])
        cur.execute( f'select "user"."user_id", "nickname" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
        prteam = cur.fetchall()
        print(prteam)
        
        pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
        cur.execute( f'drop table "prteam";')
        
        cur_user = cur.execute(
            f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
            [cur_user_id]).fetchone()
        system_role_id = cur_user[0]
        system_role = cur_user[1]
        nickname = cur_user[2]
        cur_user_id = cur_user[3]
        
        page_header = str(system_role + " " + nickname)
        
        comment_form = CommentForm()
        
        role_id = 0
        participent=0
        if not (pruser is None):
            role_id = pruser[0]
            participent=1
        
        comment_access = 0
        if role_id == owner_role_id or role_id == member_role_id or system_role == system_role_admin_id:
            comment_access = 1
            
        comment=(cur.execute( f'SELECT "postdate", "descr" from "comment" where "comment_id" = %s;', [comment_id]).fetchone())
        postdate=comment[0]
            
        if comment_form.validate_on_submit():
            cur.execute( f'UPDATE "comment" SET "descr" = %s WHERE "comment_id" = %s;', [comment_form.descr.data, comment_id])
            return redirect(url_for('task', cur_user_id = cur_user_id, project_id = project_id, task_id=task_id))
                
        return render_template('comment_edit.html',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                project_page=project_page,
                                system_role = system_role,
                                nickname=nickname,
                                cur_user_id=cur_user_id,
                                project=project,
                                form=comment_form,
                                postdate=postdate,
                                title='Редактировать комментарий')
    
# Удалить комментарий
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/<task_id>/comment_remove/<comment_id>', methods=['GET','POST'])
def comment_remove( cur_user_id, project_id, task_id, comment_id):
    with psycopg.connect(host=app.config['DB_SERVER'], 
                            port=app.config['DB_PORT'],
                            user=app.config['DB_USER'], 
                            password=app.config['DB_PASSWORD'],
                            dbname=app.config['DB_NAME'],
                            connect_timeout=app.config['DB_TIMEOUT']) as con:
        cur = con.cursor()
        
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        if not int(current_user.id) == cur_user_id:
            return redirect(url_for('editcomment', cur_user_id=current_user.id, project_id=project_id))
        
        page_header= ""
        
        home_view=1     
        home_page=0
        project_page=0
        system_role_admin_id = 1
        owner_role_id = 1
        member_role_id = 2
        
        project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
        
        cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
            [project_id])
        cur.execute( f'select "user"."user_id", "nickname" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
        prteam = cur.fetchall()
        print(prteam)
        
        pruser = cur.execute( f'select "role_id" from "prteam" where "prteam"."user_id" = %s;', [cur_user_id]).fetchone()
        cur.execute( f'drop table "prteam";')
        
        cur_user = cur.execute(
            f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
            [cur_user_id]).fetchone()
        system_role_id = cur_user[0]
        system_role = cur_user[1]
        nickname = cur_user[2]
        cur_user_id = cur_user[3]
        
        page_header = str(system_role + " " + nickname)
        
        cur.execute( f'delete from "comment" where "comment_id" = %s', [comment_id]);
        return redirect(url_for('task', cur_user_id = cur_user_id, project_id = project_id, task_id=task_id) ) 

'''
# Добавить в проект задачу
@app.route('/<int:cur_user_id>/project/<int:project_id>/newtask', methods=['GET','POST'])
def task_add( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            return render_template('task_add.html')
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
            
            
'''
