from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
import sqlite3
import os
from user_data import db, Olympiad, Users, Profiles, Applications_for_addition_Institution, Institution, Sent_applications
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from generate_an_olympiad import Generate_something
from letter import send_email
from docx_generate import rename_docx_file
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static',url_prefix='/admin')


@admin.route('/')
@login_required
def main_admin():
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    return render_template('admin/main_admin.html', title= 'Админ панель')


@admin.route('/logout')
@login_required
def logout():
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('entry'))

@admin.route('/сompetitions')
@login_required
def сompetitions():
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    olympiads = Olympiad.query.order_by(Olympiad.date.desc()).all()
    return render_template('admin/сompetitions.html', olympiads=olympiads)

@admin.route('/сompetitions/<int:id>')
@login_required
def сompetition_detail(id):
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    olympiad = Olympiad.query.get(id)
    if not olympiad:
        abort(404)
    return render_template('admin/сompetition_detail.html', olympiad=olympiad)




generate_something = Generate_something()
@admin.route('/create-article', methods =['POST', 'GET'])
@login_required
def create_article():
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    return generate_something.generate_olympiad()


#--------------------------------------------------------------------------------------------------------------------
@admin.route('/сompetitions/<int:id>/delete')
@login_required
def сompetition_delete(id):
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

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
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

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

#----------------------------------------------------------------------------------------------------------------------
@admin.route('/requests_for_addition_EI')
@login_required
def requests_for_addition_EI():
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))
    applications_for_addition_institution = Applications_for_addition_Institution.query.order_by().all()

    return render_template('admin/requests_for_addition_EI.html', applications_for_addition_institution=applications_for_addition_institution)

@admin.route('/requests_for_addition_EI/<int:id>', methods=['GET', 'POST'])
@login_required
def requests_for_addition_EI_add(id):
    if current_user.access_level != 3:
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
    if current_user.access_level != 3:
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
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    sent_applications = Sent_applications.query.order_by().all()

    return render_template('admin/submitted_applications.html', sent_applications=sent_applications)

@admin.route('/submitted_applications/<int:id>/approve')
@login_required
def submitted_applications_OK(id):
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))

    sent_applications = Sent_applications.query.get_or_404(id)
    institution = Institution.query.get_or_404(id)
    to_email = sent_applications.email
    file_path = os.path.abspath("participation_template.docx")


    educational_institution = sent_applications.educational_institution
    institution = Institution.query.filter_by(institution_title=educational_institution).first()
    if institution:
        institution_director = institution.institution_director

    if "СОШ"  in sent_applications.educational_institution or "Гимназия"  in sent_applications.educational_institution:
        new_file_path = rename_docx_file(file_path, sent_applications.title_olympiad, sent_applications.name,
                                        sent_applications.surname, sent_applications.patronymic, institution_director, sent_applications.educational_institution,
                                         sent_applications.classe)

        send_email(subject='Документ об участии в соревновании', message='Поздравляем вы являетесь участников соревнования',
                   from_email='ayanokodji3@mail.ru',
                           to_email=to_email, password='WDt89xnDkkj2hXuz9Vy6', file_path=new_file_path)

        sent_applications.approved = 'Заявка принята'
        db.session.commit()
        return redirect('/admin/submitted_applications')
    else:
        sent_applications.approved = 'Заявка принята'
        db.session.commit()
        return redirect('/admin/submitted_applications')


@admin.route('/submitted_applications/<int:id>/delete')
@login_required
def submitted_applications_NO(id):
    if current_user.access_level != 3:
        return redirect(url_for('main_page'))
    sent_applications = Sent_applications.query.get_or_404(id)

    try:
        db.session.delete(sent_applications)
        db.session.commit()
        return redirect('/admin/submitted_applications')
    except:
        return 'При удалении статьи произошла ошибка'