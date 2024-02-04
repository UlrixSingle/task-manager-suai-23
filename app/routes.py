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

@app.route('/admin_home')
def test_connection():
    message = "Состояние неопределенно"
    
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            user_names = cur.execute(f'SELECT "nickname" FROM "user";').fetchall()
            return render_template('admin_home.html', 
                                    admin_nickname='Penguin',
                                    user_names=user_names)
        
    except Exception as e:
        message = f"Ошибка подключения: {e}"
        return message
        
    '''
    except Exception as e:
        message = f"Ошибка подключения: {e}"
    else:
        message = "Подключение успешно"
    finally:
        return message
    '''
