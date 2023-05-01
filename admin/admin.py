from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
import sqlite3
import os
from user_data import db, Admins, Olympiad, Users, Profiles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generate_an_olympiad import Generate_something
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static',url_prefix='/admin')


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
        return redirect(url_for('.main_admin'))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        admin = Admins.query.filter_by(email=email).first()
        if admin and email == admin.email and check_password_hash(admin.psw, password):
            login_admin()
            return redirect(url_for('.main_admin'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/entry.html', title='Админ-панель')

@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.entry'))

    logout_admin()

    return redirect(url_for('.entry'))

@admin.route('/сompetitions')
def сompetitions():
    if not isLogged():
        return  redirect(url_for('.entry'))
    olympiads = Olympiad.query.order_by(Olympiad.date.desc()).all()
    return render_template('admin/сompetitions.html', olympiads=olympiads)

@admin.route('/сompetitions/<int:id>')
def сompetition_detail(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    olympiad = Olympiad.query.get(id)
    if not olympiad:
        abort(404)
    return render_template('admin/сompetition_detail.html', olympiad=olympiad)




generate_something = Generate_something()
@admin.route('/create-article', methods =['POST', 'GET'])
def create_article():
    if not isLogged():
        return  redirect(url_for('.entry'))
    return generate_something.generate_olympiad()


#--------------------------------------------------------------------------------------------------------------------
@admin.route('/сompetitions/<int:id>/delete')
def сompetition_delete(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    olympiad = Olympiad.query.get_or_404(id)

    try:
        db.session.delete(olympiad)
        db.session.commit()
        return redirect('/admin/сompetitions')
    except:
        return 'При удалении статьи произошла ошибка'



@admin.route('/сompetitions/<int:id>/update', methods =['POST', 'GET'])
def olympiad_update(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    olympiad = Olympiad.query.get(id)

    if request.method == 'POST':
        olympiad.title = request.form['title']
        olympiad.introduction = request.form['introduction']
        olympiad.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/admin/сompetitions')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('admin/сompetitions_update.html', olympiad=olympiad)


#----------------------------------------------------------------------------------------------------------------------
@admin.route('/list_of_users')
def list_of_users():
    if not isLogged():
        return  redirect(url_for('.entry'))
    users = Users.query.order_by(Users.date.desc()).all()
    profiles = Profiles.query.order_by(Profiles.id.desc()).all()

    profiles_dict = {profile.id: profile for profile in profiles}
    return render_template('admin/list_of_users.html', users=users, profiles=profiles_dict)

@admin.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if not isLogged():
        return  redirect(url_for('.entry'))

    if request.method == "POST":
        if request.form['psw'] == request.form['psw2']:
            try:
                hash = generate_password_hash(request.form['psw'])
                u = Users(email=request.form['email'], psw=hash)
                db.session.add(u)
                db.session.flush()

                p = Profiles(name=request.form['name'], old=request.form['old'],
                             city=request.form['city'], user_id=u.id)
                db.session.add(p)
                db.session.commit()
            except:
                db.session.rollback()
                print("Ошибка добавления в БД")

            return redirect(url_for('.main_admin'))
        else:
            flash('Пароли не совпадают', 'error')
    return render_template('admin/create_user.html',title='Создание пользователя')


@admin.route('/list_of_users/<int:id>')
def list_of_users_detail(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    user = Users.query.get_or_404(id)
    profile = Profiles.query.get_or_404(id)

    return render_template('admin/list_of_user_detail.html', user=user, profile=profile)

@admin.route('/list_of_users/<int:id>/delete')
def list_of_users_delete(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    user = Users.query.get_or_404(id)
    profile = Profiles.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.delete(profile)
        db.session.commit()
        return redirect('/admin/list_of_users')
    except:
        return 'При удалении статьи произошла ошибка'

@admin.route('/list_of_users/<int:id>/update', methods =['POST', 'GET'])
def list_of_users_update(id):
    if not isLogged():
        return  redirect(url_for('.entry'))
    user = Users.query.get(id)
    profile = Profiles.query.get(id)

    if request.method == 'POST':
        user.email = request.form['email']
        profile.name = request.form['name']
        profile.old = request.form['old']
        profile.city = request.form['city']


        try:
            db.session.commit()
            return redirect('/admin/list_of_users')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('admin/list_of_users_update.html', user=user, profile=profile)

#----------------------------------------------------------------------------------------------------------------------