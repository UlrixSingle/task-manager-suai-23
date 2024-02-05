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
    
@app.route('/user_home', methods=['GET','POST'])
def get_home_user():
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            admin_names = []
            user_names = []
            return render_template('home.html',
                                    system_role_id=2,
                                    system_role = 'Пользователь',
                                    nickname='Knot',
                                    admin_names=admin_names,
                                    user_names=user_names,
                                    project_names=[])
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
    
    
# Главная страница администратора
@app.route('/admin_home', methods=['GET','POST'])
def get_home_admin():
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


@app.route('/profile/<user_login>', methods=['GET','POST'])
def get_profile( user_login):
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            user = cur.execute(
                f'SELECT "usr"."name", "usr"."nickname", "usr"."second_name", "usr"."first_name", "usr"."surname", "usr"."mail", "usr"."phone", "usr"."descr", "usr"."login" FROM (SELECT * FROM "system_role", "user" WHERE "user"."system_role_id" = "system_role"."system_role_id") "usr" WHERE  "login" = %s;',
                [user_login]).fetchone()
                
            return render_template('profile.html',
                                    system_role_id=2,
                                    system_role = 'Пользователь',
                                    nickname='Knot',
                                    login='user2',
                                    user=user)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message


