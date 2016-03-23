import sqlite3
from flask import Flask, redirect, url_for, render_template, request
from lib import runemaker

# config
DEBUG = True

# Create the app
app = Flask(__name__)
app.config.from_object(__name__)

# ROUTING
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runemaker')
def show_entries():
    champNameZippedList = runemaker.get_champion_list()
    champNameZippedList.sort(key=lambda x: x[1])
    return render_template('runemaker.html', champNameZippedList=champNameZippedList)
    
@app.route('/getRunePages', methods=['POST'])
def get_rune_pages():
    champNames = request.form.getlist('champs')
    try:
        numPages = int(request.form['numPages'])
    except ValueError:
        return render_template('error.html')
    
    if champNames == None or numPages == None:
        return render_template('error.html')
         
    runeData = runemaker.get_runepages(champNames, numPages)

    return render_template('results.html', champNames=champNames, numPages=numPages, results=runeData['results'], leftOut=runeData['leftOut'])

@app.route('/rolemaker')
def show_roles():
    return render_template('rolemaker.html')
    
if __name__=='__main__':
    app.run()
