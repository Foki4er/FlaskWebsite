from flask import Flask, render_template, url_for, request, g, redirect, flash
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from admin.admin import admin

DATABASE = 'tmp/app.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'app.db')))

app.register_blueprint(admin, url_prefix = '/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'entry'

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


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
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/')
def main_page():
    return render_template("main_page.html", menu = dbase.getMenu())

# @app.route('/create-article', methods =['POST', 'GET'])
# def create_article():
#     if request.method == 'POST':
#         res = dbase.create_article(request.form['title'], request.form['text'])
#     return render_template('create-article.html', menu = dbase.getMenu())


@app.route('/сompetitions')
@login_required
def сompetitions():
    return render_template('сompetitions.html', menu = dbase.getMenu(), posts = dbase.сompetitions())


@app.route('/сompetitions/post/<int:id_post>')
@login_required
def сompetitions_detail(id_post):
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu = dbase.getMenu(),title=title,post=post)


@app.route("/entry", methods=["POST", "GET"])
def entry():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))


    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template("entry.html", menu=dbase.getMenu(), title="Авторизация")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if request.form['password'] == request.form["confirm_password"]:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(url_for('entry'))
            else:
                flash('Ошибка при добавлении в БД', 'error')
        else:
            flash('Неверное заполнены поля', 'error')

    return render_template("registration_new.html", menu = dbase.getMenu(), title='Регистрация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('entry'))


@app.route('/profile')
@login_required
def profile():
    return f"""<a href="{url_for('logout')}">Выйти из профиля</a>
                user info: {current_user.get_id()}"""



if __name__ == '__main__':
    app.run(debug=True)