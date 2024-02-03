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
    con = None
    try:
        con = psycopg.connect(host=app.config['DB_SERVER'], 
                              user=app.config['DB_USER'], 
                              password=app.config['DB_PASSWORD'],
                              dbname=app.config['DB_NAME'])
        cur = con.cursor()
        #cur.execute('SELECT * FROM my_table')

    except Exception as e:
        message = f"Ошибка подключения: {e}"
    else:
        message = "Подключение успешно"
    finally:
        if con:
            con.close()
        return message
