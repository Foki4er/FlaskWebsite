from flask import Flask, render_template, url_for, request, g, redirect, flash
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from admin.admin import admin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from user_data import db, Users, Profiles, Olympiad
from registration_login import Register_login
from generate_an_olympiad import Generate_something

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'entry'

register_or_login = Register_login()

@app.route('/registration', methods=('GET', 'POST'))
def registeration():
    return register_or_login.register()

@app.route("/entry", methods=["POST", "GET"])
def entry():
    return register_or_login.login()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def main_page():
    return render_template("main_page.html")

@app.route('/сompetitions')
@login_required
def сompetitions():
    olympiad = Olympiad.query.order_by(Olympiad.date).all()
    return render_template('сompetitions.html', olympiad=olympiad)



generate_something = Generate_something()

@app.route('/create-article', methods =['POST', 'GET'])
@login_required
def create_article():
    return generate_something.generate_olympiad()





#
#
# @app.route('/сompetitions/post/<int:id_post>')
# @login_required
# def сompetitions_detail(id_post):
#     title, post = dbase.getPost(id_post)
#     if not title:
#         abort(404)
#
#     return render_template('post.html', menu = dbase.getMenu(),title=title,post=post)
#
#

#
#



# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("Вы вышли из аккаунта", "success")
#     return redirect(url_for('entry'))






if __name__ == '__main__':
    app.run(debug=True)