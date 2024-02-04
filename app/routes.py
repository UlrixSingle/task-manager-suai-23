from flask import request
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

@app.route('/testdb')
def test_connection():
    try:
        with psycopg.connect(host=app.config['DB_SERVER'], 
                              port=app.config['DB_PORT'],
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'],
                              connect_timeout=app.config['DB_TIMEOUT']) as con:
            cur = con.cursor()
            
            for row in cur.execute('SELECT * FROM "user";'):
                print(f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} ')

    except Exception as e:
        message = f"Ошибка подключения: {e}"
    else:
        message = "Подключение успешно"
    finally:
        return message
