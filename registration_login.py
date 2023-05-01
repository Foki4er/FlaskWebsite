from flask import redirect, render_template, request, url_for, flash
from Repositores import UserRepository
from Models.Users import UserPost, Profiles
from user_data import db
from flask_login import login_user, current_user


class Register_login:

    def __init__(self):
        self.__user_repository: UserRepository = UserRepository(db.session)

    def register(self):
        if request.method == "POST":
            if request.form['psw'] == request.form['psw2']:
                user = UserPost(
                    email=request.form['email'],
                    psw=request.form['psw'],
                    pr=Profiles(
                        name=request.form['name'],
                        old=request.form['old'],
                        city=request.form['city']
                    )
                )
                self.__user_repository.add(user)

                return redirect(url_for('main_page'))
            else:
                flash('Пароли не совпадают', 'error')

        return render_template("registration_new.html", title="Регистрация")

    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))

        if request.method == "POST":
            email = request.form['email']
            password = request.form['psw']
            user = self.__user_repository.get_by_email(email)
            if user and user.check_password(password):
                rm = True if request.form.get('remainme') else False
                login_user(user, remember=rm)
                return redirect(request.args.get('next') or url_for('main_page'))

            flash("Неверный логин/пароль", "error")

        return render_template("entry.html", title="Авторизация")
