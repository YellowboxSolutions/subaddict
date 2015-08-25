from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing


DATABASE = '/vagrant/srv/subattic.db'
DEBUG = True
SECRET_KEY = 'a secret key'
USERNAME = 'dbuser'
PASSWORD = 'dbpass'

app = Flask(__name__)
app.config.from_object(__name__)

class ServicePoint():

    def __init__(self, row):
        try:
            self.id = row['id']
            self.agreement_number = row['Agreement']
            self.service_point = row['ServicePoint']
        except AttributeError:
            raise AttributeError, "Required column missing"

def db_connect():
    """Returns instance of database"""
    r =  sqlite3.connect(app.config['DATABASE'])
    r.row_factory = sqlite3.Row
    return r


def db_init():
   """Initializes the database"""
   with closing(db_connect()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
           db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = db_connect()
    

@app.teardown_request
def after_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def welcome():
    return render_template('welcome.html', items=items)


@app.route('/sp/list/')
@app.route('/sp/list/<query_type>/<query_value>')
def sp_list(query_type=None, query_value=None):
    if query_type is not None:
        cur = g.db.execute('select * from ServicePoints where ? = ?', (query_type, query_value))
    else:
        cur = g.db.execute('select * from ServicePoints limit 25')
    service_points = [ServicePoint(row) for row in cur.fetchall()]
    return render_template('list.html', service_points=service_points)


@app.route('/sp/view/<id>')
def sp_view(id):
    cur = g.db.execute('select * from ServicePoints where id = ?', (id, ))
    service_point = ServicePoint(cur.fetchone())
    return render_template('view.html', service_point=service_point)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
