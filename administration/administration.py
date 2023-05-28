from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
import sqlite3
import os
from user_data import db, Olympiad, Users, Profiles, Applications_for_addition_Institution, Institution, Sent_applications, Science_application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generate_an_olympiad import Generate_something
from letter import send_email

administration = Blueprint('administration', __name__, template_folder='templates', static_folder='static',url_prefix='/administration')

@administration.route('/')
@login_required
def main_administration():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    return render_template('administration/main_administration.html', title= 'Панель администратора')

@administration.route('/competitive_works')
@login_required
def competitive_works():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    application = Science_application.query.order_by().all()
    sent_applications = Sent_applications.query.order_by().all()
    return render_template('administration/competitive_works.html',sent_applications=sent_applications, application=application )


@administration.route('/competitive_works/<int:id>', methods=['GET', 'POST'])
@login_required
def estimate(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    application = Science_application.query.get(id)
    sent_applications = Sent_applications.query.get_or_404(id)

    if request.method == 'POST':
        job_evaluation = request.form.get('field13')
        application.job_evaluation = job_evaluation
        sent_applications.status = 'Оценено'
        db.session.commit()
        return redirect('/administration/competitive_works')

    return render_template('administration/estimate.html', application=application)


@administration.route('/logout')
@login_required
def logout():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('entry'))