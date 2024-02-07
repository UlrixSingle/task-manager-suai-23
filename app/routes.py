from app.forms import RegistrationForm
from flask import request
from flask import render_template, redirect, flash, url_for
from app import app
import psycopg

# Корневой тест
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        print("register (GET)")
    elif request.method == 'POST':
        print("register (POST)")
    else:
        print("register Unknown")
    
    if request.method == 'GET':
        return "Hello, World! (GET)"
    elif request.method == 'POST':
        return "Hello, World! (POST)"
    else:
        return "Unknown"

'''
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
                                home_page=home_page)
    
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

# Приветствующая страница
@app.route('/welcome', methods=['GET'])
def welcome():
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            #cur = con.cursor()
            
            page_header="Добро пожаловать!"
            
            home_view=1
            home_page=0
            
            cur_user_id=1
            
        return render_template('welcome.html',
                                page_header=page_header,
                                home_view=home_view,
                                home_page=home_page,
                                cur_user_id=cur_user_id)
    
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Главная страница
@app.route('/<int:cur_user_id>/home', methods=['GET','POST'])
def home( cur_user_id):
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
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
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
            
            page_header=""
            
            home_view=1
            home_page=0
            project_page=1
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            stages=cur.execute( f'select * from "stage"').fetchall()
            
            tasks=[]
            tasks_n=[]
            for i in range(len(stages)):
                task_list = [cur.execute( f'select "task"."task_id", "task"."name" as "taskname", "descr", "begindate", "enddate", "stage_id", "task"."priority_id", "priority"."name" as "priority_name", "colour", "weight" from "task" join "priority" on "task"."priority_id" = "priority"."priority_id" where "task"."project_id" = %s and "task"."stage_id" = %s;', [project_id, i+1]).fetchall()]
                tasks += task_list
                tasks_n += [len(task_list)]
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
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
                                    tasks_maxlength=max(tasks_n))
        
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
            
            page_header= ""
            
            home_view=1
            home_page=0
            project_page=0
            system_role_admin_id = 1
            owner_role_id = 1
            
            project = cur.execute( f'select "project_id", "name" from "project" where "project_id" = %s', [project_id]).fetchone()
            task = cur.execute( f'select * from "task" where "task_id" = %s', [task_id]).fetchone()
            
            comments = cur.execute( f'select "comment_id", "postdate", "user"."nickname", "comment"."descr", "user"."user_id" from "comment" join "user" on "comment"."user_id" = "user"."user_id" where "comment"."task_id" = %s order by "comment"."comment_id";', [task_id]).fetchall()
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            edit_access = 1
            comment_access = 1
            
            page_header = str(system_role + " " + nickname)
            
            return render_template('task.html',
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project,
                                    task=task,
                                    comments=comments,
                                    edit_access=edit_access,
                                    comment_access=comment_access)

    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
# Добавить в проект задачу
@app.route('/<int:cur_user_id>/project/<int:project_id>/task/add', methods=['GET','POST'])
def task_add( cur_user_id, project_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            page_header="Создание новой задачи"
            
            home_view=1
            home_page=0
            
            project = cur.execute( f'select "project_id", "name", "descr" from "project" where "project_id" = %s', [project_id]).fetchone()
            
            cur.execute( f'create table "prteam" as select "user_id", "project_id", "role"."name" as "role_name", "job", "role"."role_id" from "role" join (select * from "team" where "project_id" = %s) "raw" on "role"."role_id" = "raw"."role_id";',
                [project_id])
            cur.execute( f'select "user"."user_id", "nickname" from "user" join "prteam" on "user"."user_id" = "prteam"."user_id";')
            prteam = cur.fetchall()
            cur.execute( f'drop table "prteam";')
            
            task_form = TaskAddForm()
            
            task_form.stage.choices = cur.execute( f'SELECT * FROM stage;').fetchall()
            task_form.priority.choices = cur.execute( f'SELECT * FROM priority;').fetchall()
            task_form.user.choices = prteam
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            if reg_form.validate_on_submit():
                # создать запись в базе данных
                return f'Задача {reg_form.nickname.data} добавлена'
                    
            return render_template( 'task_add.html', 
                                    page_header=page_header,
                                    home_view=home_view,
                                    home_page=home_page,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    project=project,
                                    title='Новая задача', 
                                    form=task_form)

    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
