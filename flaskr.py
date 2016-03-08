import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# config
DATABASE        = '/tmp/flaskr.db'
DEBUG           = True
SECRET_KEY      = 'development key'
USERNAME        = 'admin'
PASSWORD        = 'default'

# Create our little application
app = Flask(__name__)
app.config.from_object(__name__)
# from_object will look at the given object and then look for all uppercase vars define there.
# We use the config defined in this file, above. We could move it to another file though.
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# This would get the config file from an env var called FLASKR_SETTINGS

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
        
def init_db():
    with closing(connect_db()) as db: # closing(...) keeps connection open only for the block.
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
# g is the special object Flask provides for us. It stores info for 1 request only and is available
# from within each function. 
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# ROUTING
        
@app.route('/')
def show_entries():
    query = 'SELECT title, text FROM entries ORDER BY id DESC'
    cur = g.db.execute(query)
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    
    # Note from tutorial - use the ?s to bind sql and flask will handle SQL injection automatically.
    query = 'INSERT INTO entries (title, text) values (?, ?)'
    g.db.execute(query, [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else: # valid
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None) # This pops 'logged_in' if present, else does nothing.
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
if __name__=='__main__':
    app.run()