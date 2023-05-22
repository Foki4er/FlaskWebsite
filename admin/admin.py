from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
import sqlite3
import os
from user_data import db, Olympiad, Users, Profiles, Applications_for_addition_Institution, Institution, Sent_applications
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generate_an_olympiad import Generate_something
from letter import send_email
from pdf_generate import rename_pdf_file
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static',url_prefix='/admin')


@admin.route('/')
@login_required
def main_admin():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    return render_template('admin/main_admin.html', title= 'Админ панель')


# @admin.route('/entry', methods=["POST", "GET"])
# def entry():
#     if isLogged():
#         return redirect(url_for('.main_admin'))
#
#     if request.method == "POST":
#         email = request.form['email']
#         password = request.form['psw']
#         admin = Admins.query.filter_by(email=email).first()
#         if admin and email == admin.email and check_password_hash(admin.psw, password):
#             login_admin()
#             return redirect(url_for('.main_admin'))
#         else:
#             flash("Неверная пара логин/пароль", "error")
#
#     return render_template('admin/entry.html', title='Админ-панель')

# @admin.route('/logout', methods=["POST", "GET"])
# def logout():
#     if not isLogged():
#         return redirect(url_for('.entry'))
#
#     logout_admin()
#
#     return redirect(url_for('.entry'))
@admin.route('/logout')
@login_required
def logout():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('entry'))

@admin.route('/сompetitions')
@login_required
def сompetitions():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
    olympiads = Olympiad.query.order_by(Olympiad.date.desc()).all()
    return render_template('admin/сompetitions.html', olympiads=olympiads)

@admin.route('/сompetitions/<int:id>')
@login_required
def сompetition_detail(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))

    olympiad = Olympiad.query.get(id)
    if not olympiad:
        abort(404)
    return render_template('admin/сompetition_detail.html', olympiad=olympiad)




generate_something = Generate_something()
@admin.route('/create-article', methods =['POST', 'GET'])
@login_required
def create_article():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
    return generate_something.generate_olympiad()


#--------------------------------------------------------------------------------------------------------------------
@admin.route('/сompetitions/<int:id>/delete')
@login_required
def сompetition_delete(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
    olympiad = Olympiad.query.get_or_404(id)

    try:
        db.session.delete(olympiad)
        db.session.commit()
        return redirect('/admin/сompetitions')
    except:
        return 'При удалении статьи произошла ошибка'



@admin.route('/сompetitions/<int:id>/update', methods =['POST', 'GET'])
@login_required
def olympiad_update(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
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
@login_required
def list_of_users():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
    users = Users.query.order_by(Users.date.desc()).all()
    profiles = Profiles.query.order_by(Profiles.id.desc()).all()

    profiles_dict = {profile.id: profile for profile in profiles}
    return render_template('admin/list_of_users.html', users=users, profiles=profiles_dict)

@admin.route('/create_user', methods=('GET', 'POST'))
@login_required
def create_user():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))

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
@login_required
def list_of_users_detail(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
    user = Users.query.get_or_404(id)
    profile = Profiles.query.get_or_404(id)

    return render_template('admin/list_of_user_detail.html', user=user, profile=profile)

@admin.route('/list_of_users/<int:id>/delete')
@login_required
def list_of_users_delete(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
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
@login_required
def list_of_users_update(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    # if not isLogged():
    #     return  redirect(url_for('.entry'))
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
@admin.route('/requests_for_addition_EI')
@login_required
def requests_for_addition_EI():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    applications_for_addition_institution = Applications_for_addition_Institution.query.order_by().all()

    return render_template('admin/requests_for_addition_EI.html', applications_for_addition_institution=applications_for_addition_institution)

@admin.route('/requests_for_addition_EI/<int:id>', methods=['GET', 'POST'])
@login_required
def requests_for_addition_EI_add(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    applications_for_addition_institution = Applications_for_addition_Institution.query.get_or_404(id)

    if request.method == 'POST':
        # получить данные из формы
        institution_title = request.form.get('institution_title')
        institution_director = request.form.get('institution_director')
        institution_email = request.form.get('institution_email')

        # создать объект Institution
        institution = Institution(
            institution_title=institution_title,
            institution_director=institution_director,
            institution_email=institution_email
        )

        # добавить объект Institution в базу данных
        db.session.add(institution)
        db.session.delete(applications_for_addition_institution)
        db.session.commit()

        # перенаправить пользователя на страницу со списком заявок на добавление учебных заведений
        return redirect(url_for('admin.requests_for_addition_EI'))

    return render_template('admin/requests_for_addition_EI_add.html', applications_for_addition_institution=applications_for_addition_institution)

@admin.route('/requests_for_addition_EI/<int:id>/delete')
@login_required
def requests_for_addition_EI_delete(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    applications_for_addition_institution = Applications_for_addition_Institution.query.get_or_404(id)

    try:
        db.session.delete(applications_for_addition_institution)
        db.session.commit()
        return redirect('/admin/requests_for_addition_EI')
    except:
        return 'При удалении статьи произошла ошибка'

#---------------------------------------------------------------------------------------------------------
@admin.route('/submitted_applications')
@login_required
def submitted_applications():
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    sent_applications = Sent_applications.query.order_by().all()

    return render_template('admin/submitted_applications.html', sent_applications=sent_applications)

@admin.route('/submitted_applications/<int:id>/approve')
@login_required
def submitted_applications_OK(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))

    sent_applications = Sent_applications.query.get_or_404(id)
    to_email = sent_applications.email
    file_path = os.path.abspath("check.pdf")
    print(file_path)
    new_file_path = rename_pdf_file(file_path, sent_applications.title_olympiad, sent_applications.name,sent_applications.surname,sent_applications.patronymic)
    try:
        send_email(subject='Test email', message='This is a test email from Python', from_email='ayanokodji3@mail.ru',
                   to_email=to_email, password='WDt89xnDkkj2hXuz9Vy6', file_path=new_file_path)
        sent_applications.approved = 'Заявка принята'
        db.session.commit()
        return redirect('/admin/submitted_applications')
    except:
        return 'При принятии запроса произошла ошибка'

@admin.route('/submitted_applications/<int:id>/delete')
@login_required
def submitted_applications_NO(id):
    if current_user.access_level != 2:
        return redirect(url_for('main_page'))
    sent_applications = Sent_applications.query.get_or_404(id)

    try:
        db.session.delete(sent_applications)
        db.session.commit()
        return redirect('/admin/submitted_applications')
    except:
        return 'При удалении статьи произошла ошибка'