from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
import sqlite3
import os
from FDataBase import FDataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@admin.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

def isLogged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def main_admin():
    if not isLogged():
        return  redirect(url_for('.entry'))

    return render_template('admin/main_admin.html', title= 'Админ панель')


@admin.route('/entry', methods=["POST", "GET"])
def entry():
    if isLogged():
        return  redirect(url_for('.main_admin'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.main_admin'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/entry.html', title='Админ-панель')

@admin.route('/create-article', methods =['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        res = dbase.create_article(request.form['title'], request.form['text'])
    return render_template('admin/create-article.html', menu = dbase.getMenu())

@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.entry'))

    logout_admin()

    return redirect(url_for('.entry'))