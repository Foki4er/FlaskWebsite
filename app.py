from flask import Flask, render_template, url_for, request, g, redirect, flash, abort
import sqlite3
import os
#from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from UserLogin import UserLogin
from admin.admin import admin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from administration.administration import administration
from user_data import db, Users, Olympiad, Profiles, Applications_for_addition_Institution, Sent_applications, Science_application
from registration_login import Register_login
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(administration)
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

@app.route('/private_office', methods=['GET', 'POST'])
@login_required
def private_office():
    user = current_user
    profile = user.profile
    sent_application = Sent_applications.query.all()

    profile = Profiles.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        user.email = request.form['email']
        profile.name = request.form['name']
        profile.surname = request.form['surname']
        profile.patronymic = request.form['patronymic']
        profile.old = request.form['old']
        profile.city = request.form['city']
        profile.educational_institution = request.form['educational_institution']
        profile.phone_number = request.form['phone_number']
        db.session.commit()
    return render_template("private_office.html",user=user,profile=profile, sent_application=sent_application)

@app.route('/my_applications', methods=['GET', 'POST'])
@login_required
def my_applications():
    user = Users.query.filter_by(email=current_user.email).first()
    sent_application = Sent_applications.query.filter_by(email=user.email).all()

    return render_template("my_applications.html", user=user, sent_application=sent_application)


@app.route('/create_educational_institution', methods=['GET', 'POST'])
def create_educational_institution():
    if request.method == 'POST':
        institution_name = request.form['educational_institution']
        institution = Applications_for_addition_Institution(institution_name=institution_name)
        db.session.add(institution)
        db.session.commit()
        flash('Заявка на добавление учебного заведения отправлена.')
        return redirect(url_for('create_educational_institution'))
    return render_template("create_educational_institution.html")


@app.route('/сompetitions')
@login_required
def сompetitions():
    olympiads = Olympiad.query.order_by(Olympiad.date.desc()).all()
    return render_template('сompetitions.html', olympiads=olympiads)

@app.route('/сompetitions/<int:id>')
@login_required
def сompetition_detail(id):
    olympiad = Olympiad.query.get(id)
    if not olympiad:
        abort(404)
    return render_template('сompetition_detail.html', olympiad=olympiad)

@app.route('/сompetitions/<int:id>/application', methods=['GET', 'POST'])
@login_required
def сompetition_application(id):
    olympiad = Olympiad.query.get(id)
    user = current_user
    profile = user.profile

    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        old = request.form['old']
        city = request.form['city']
        educational_institution = request.form['educational_institution']

        words = educational_institution.split()
        if words[0] == "СОШ" or words[0] == "Гимназия":
            classe = request.form['class']
        else:
            classe = request.form['course']


        phone_number = request.form['phone_number']
        email = request.form['email']
        title_olympiad = olympiad.title


        new_application = Sent_applications(title_olympiad=title_olympiad, name=name, surname=surname, patronymic=patronymic, old=old, city=city,
                                             educational_institution=educational_institution, classe=classe, phone_number=phone_number, email=email)
        try:
            db.session.add(new_application)
            db.session.commit()
            flash('Заявка успешно отправлена!')
        except:
            db.session.rollback()
            flash('Вы уже подали заявку на эту олимпиаду.')



    return render_template('сompetition_application.html', olympiad=olympiad, user=user, profile=profile)






@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('entry'))


#------------------------------------------------------------------------

@app.route('/my_applications/submit_a_job', methods=['GET','POST'])
@login_required
def submit_a_job():
    sent_application = Sent_applications.query.all()
    if request.method == 'POST':
        title_olympiad = request.form.get('title_olympiad')
        email = request.form.get('email')
        purpose_project = request.form.get('goal')
        project_tasks = request.form.get('tasks')
        product_purpose = request.form.get('purpose')
        scientific_novelty = request.form.get('novelty')
        rationale_conducting_research = request.form.get('justification')
        main_technical_parameters = request.form.get('tech_params')
        design_requirements = request.form.get('constructive_requirements')
        patent_requirements = request.form.get('patent_requirements')
        application_area = request.form.get('field9')
        volume_off_budget_investments = request.form.get('field10')
        available_analogues = request.form.get('field11')
        project_commercialization_plan = request.form.get('field12')
        job_evaluation = ''  # You can set the default value or leave it empty

        # Create a new instance of the Science_application model
        new_application = Science_application(
            title_olympiad=title_olympiad,
            email=email,
            purpose_project=purpose_project,
            project_tasks=project_tasks,
            product_purpose=product_purpose,
            scientific_novelty=scientific_novelty,
            rationale_conducting_research=rationale_conducting_research,
            main_technical_parameters=main_technical_parameters,
            design_requirements=design_requirements,
            patent_requirements=patent_requirements,
            application_area=application_area,
            volume_off_budget_investments=volume_off_budget_investments,
            available_analogues=available_analogues,
            project_commercialization_plan=project_commercialization_plan,
            job_evaluation=job_evaluation
        )

        # Add the new application to the database
        db.session.add(new_application)
        db.session.commit()


        return redirect('/my_applications')
    else:
        return render_template('submit_a_job.html', sent_application=sent_application)




if __name__ == '__main__':
    app.run(debug=True)