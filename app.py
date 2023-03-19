from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/сompetitions')
def сompetitions():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("сompetitions.html", articles=articles)

@app.route('/сompetitions/<int:id>')
def сompetitions_detail(id):
    article = Article.query.get(id)
    return render_template("сompetitions_detail.html", article=article)

@app.route('/create-article', methods = ['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/сompetitions')
        except:
            return 'При добавлении произошла ошибка'
    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run(debug=True)