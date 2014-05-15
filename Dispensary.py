# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Dispensary.db'),
    DEBUG=True,
    SECRET_KEY='1234567890123456789',
    USERNAME='root', # Use this in the login screen.
    PASSWORD='root'  # Use this in the login screen.
    # We'll port this over to a new Database later.
))
app.config.from_envvar('DISPENSARY_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST']) #add
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into Users (Sno, RegNo, \'First Name\', \'Middle Name\',\'Last Name\', \'Blood Group\', \'Date of Birth\', Age, Type, \'Phone number\', Address, email) values (?,?,?,?,?,?,?,?,?,?,?,?)',
        [request.form['Sno'], request.form['RegNo'],request.form['FirstName'],request.form['MiddleName'],request.form['LastName'],request.form['BloodGroup'],request.form['DateOfBirth'],request.form['Age'],request.form['Type'],request.form['PhoneNumber'],request.form['text'],request.form['email']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))#show_entries

# @app.route('/reg', methods=['POST']) #reg
# def add_user():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into Users (Sno, RegNo, First Name, Middle Name,Last Name, Blood Group, Date of Birth, Age, Type, Phone number, Address, email) values (?, ?,?,?,?,?,?,?,?,?,?,?)',
#         [request.form['Sno'], request.form['RegNo'],request.form['FirstName'],request.form['MiddleName'],request.form['LastName'],request.form['BloodGroup'],request.form['DateOfBirth'],request.form['Age'],request.form['Type'],request.form['PhoneNumber'],request.form['text'],request.form['email']])

#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error) #login.html

@app.route('/inventory')
def inventory():
    db = get_db()
    cur = db.execute('select * from Pharmacy order by Sno asc')
    entries = cur.fetchall()
    return render_template('pharmventory.html',entries = entries)

@app.route('/insert',methods=['GET','POST'])
def insert():
    db=get_db()
    sno=request.form['Sno']
    name=request.form['Name']
    quantity=request.form['qty']
    batchno=request.form['bno']
    mfg=request.form['mfgdate']
    exp=request.form['expdate']
    db.execute('insert into pharmacy values(?,?,?,?,?,?)',[sno,name,quantity,batchno,mfg,exp])
    db.commit()
    flash('New entry successfully inserted')
    return redirect(url_for('inventory'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))#show_entries.html

if __name__ == '__main__':
    app.debug = True
    app.run()
