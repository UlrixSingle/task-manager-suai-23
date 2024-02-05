from flask import request
from flask import render_template
from app import app
import psycopg

@app.route('/', methods=['GET','POST'])
def index():
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
    
# Главная страница администратора
@app.route('/<cur_user_id>/home', methods=['GET','POST'])
def home( cur_user_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            system_role_admin_id = 1
            system_role_user_id = 2
            
            cur_user = cur.execute(
                f'SELECT "usr"."system_role_id", "usr"."name", "usr"."nickname", "usr"."user_id" FROM (select * from "user" natural full outer join "system_role") "usr" WHERE  "user_id" = %s;',
                [cur_user_id]).fetchone()
            system_role_id = cur_user[0]
            system_role = cur_user[1]
            nickname = cur_user[2]
            cur_user_id = cur_user[3]
            
            admins = []
            users = []
            projects = []
            if( system_role_id == 1):
                admins = cur.execute(f'SELECT "user_id", "nickname" FROM "user" WHERE system_role_id = %s;', [system_role_admin_id]).fetchall()
                users = cur.execute(f'SELECT "user_id", "nickname" FROM "user" WHERE system_role_id = %s;', [system_role_user_id] ).fetchall()
                projects = cur.execute(f'SELECT "project_id", "name" FROM "project"').fetchall()
            
            return render_template('home.html',
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
    
@app.route('/<cur_user_id>/announce', methods=['GET','POST'])
def announce( cur_user_id):
    return 'OK'
    
@app.route('/<cur_user_id>/exit', methods=['GET','POST'])
def exit( cur_user_id):
    return 'OK'

@app.route('/<cur_user_id>/profile/<user_id>', methods=['GET','POST'])
def profile( cur_user_id, user_id):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
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
            
            return render_template('profile.html',
                                    system_role_id=system_role_id,
                                    system_role = system_role,
                                    nickname=nickname,
                                    cur_user_id=cur_user_id,
                                    user=user)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message

@app.route('/<cur_user_id>/project/<project_id>', methods=['GET','POST'])
def project( cur_user_id, project_id):
    return 'OK'

