from flask import redirect, render_template, request, url_for, flash
from user_data import Olympiad, db
from werkzeug.security import generate_password_hash
from flask_login import login_required

class Generate_something:
    def generate_olympiad(self):
        if request.method == 'POST':
            title = request.form['title']
            introduction = request.form['introduction']
            text = request.form['text']

            olympiad = Olympiad(title=title, introduction=introduction, text=text)
            try:
                db.session.add(olympiad)
                db.session.commit()
                return redirect('/admin/сompetitions')
            except:
                return 'При добавлении статьи произошла ошибка'

        return render_template('admin/create-article.html')