class Register_login:
    def register(self):
        institutions = Institution.query.all()
        if request.method == "POST":
            if request.form['psw'] == request.form['psw2']:
                try:

                    hash = generate_password_hash(request.form['psw'])
                    u = Users(email=request.form['email'], psw=hash)
                    db.session.add(u)
                    db.session.flush()

                    p = Profiles(name=request.form['name'],surname=request.form['surname'], patronymic=request.form['patronymic'],
                                 old=request.form['old'],city=request.form['city'], educational_institution=request.form['educational_institution'],
                                 phone_number=request.form['phone_number'], user_id=u.id)
                    db.session.add(p)
                    db.session.commit()
                except:
                    db.session.rollback()
                    print("Ошибка добавления в БД")

                return redirect(url_for('main_page'))
            else:
                flash('Пароли не совпадают', 'error')

        return render_template("registration_new.html", title="Регистрация", institutions=institutions)


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_title = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Institution {self.id}>"





{% extends 'base.html' %}

{% block title %}
{{ title }}
{% endblock %}

{% block body %}
<head>
<link rel="stylesheet" href="{{ url_for('static', filename='css/error.css') }}">

{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class=flashes>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
    </head>
<head>
<link rel="stylesheet" href="{{ url_for('static', filename='css/regist_new.css') }}">
</head>

<form action="" method="post" class="form-contact">
  <p><label>Фамилия: </label> <input type="text" name="surname" value="" required />
  <p><label>Имя: </label> <input type="text" name="name" value="" required />
  <p><label>Отчество: </label> <input type="text" name="patronymic" value="" required />
  <p><label>Возраст: </label> <input type="text" name="old" value="" required />
  <p><label>Учебное заведение:</label>
<select name="educational_institution" required style="width: 300px;">
  {% for institution in institutions %}
    <option value="{{ institution.institution_title }}">{{ institution.institution_title }}</option>
  {% endfor %}
</select></p>
  <p><label>Город: </label> <input type="text" name="city" value="" required />
  <p><label>Email: </label> <input type="text" name="email" value="" required />
  <p><label>Номер телефона: </label> <input type="text" name="phone_number" value="" required />
  <p><label>Пароль: </label> <input type="password" name="psw" value="" required />
  <p><label>Повтор пароля: </label> <input type="password" name="psw2" value="" required />
  <p><input type="submit" value="Регистрация" />
</form>

{% endblock %}