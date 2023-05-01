from flask import redirect, render_template, request, url_for, flash
from user_data import Users, Profiles, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

class Register_login:
    def register(self):
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
            user = Users.query.filter_by(email=email).first()
            if user and check_password_hash(user.psw, password):
                rm = True if request.form.get('remainme') else False
                login_user(user, remember=rm)
                return redirect(request.args.get('next') or url_for('main_page'))

            flash("Неверный логин/пароль", "error")

        return render_template("entry.html", title="Авторизация")
