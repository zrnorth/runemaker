import sqlite3
from flask import Flask, redirect, url_for, render_template, request, jsonify
from lib import rolemaker
from lib import runemaker

# config
DEBUG = True

# Create the app
application = Flask(__name__)
application.config.from_object(__name__)

# ROUTING
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/runemaker')
def show_entries():
    champNameZippedList = runemaker.get_champion_list()
    champNameZippedList.sort(key=lambda x: x[1])
    return render_template('runemaker.html', champNameZippedList=champNameZippedList)
    
@application.route('/getRunePages', methods=['POST'])
def get_rune_pages():
    champNames = request.form.getlist('champs')
    try:
        numPages = int(request.form['numPages'])
    except ValueError:
        return render_template('error.html')
    
    if champNames == None or numPages == None:
        return render_template('error.html')
         
    runeData = runemaker.get_runepages(champNames, numPages)

    return render_template('rune_results.html', champNames=champNames, numPages=numPages, results=runeData['results'], leftOut=runeData['leftOut'])

@application.route('/rolemaker')
def show_roles():
    return render_template('rolemaker.html')

@application.route('/getRoles', methods=['POST'])
def get_roles():
    role = request.form['roleName']
    num = int(request.form['num'])

    aggStats, roleStats = rolemaker.get_role_stats(role)
    champPool = rolemaker.make_champ_pool(role, roleStats, num)

    return render_template('role_results.html', num=num, champPool=champPool, roleStats=roleStats)

@application.route('/_getRolesAJAX')
def get_roles_ajax():
    role = request.args.get('roleName', '', type=str)
    num = request.args.get('num', 0, type=int)

    aggStats, roleStats = rolemaker.get_role_stats(role)
    champPool = rolemaker.make_champ_pool(role, roleStats, num)
    return jsonify(num=num, champPool=champPool, roleStats=roleStats)

if __name__=='__main__':
    application.run()
