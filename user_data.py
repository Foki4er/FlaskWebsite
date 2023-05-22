from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    access_level = db.Column(db.Integer, default=1)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    surname = db.Column(db.String(50), nullable=True)
    patronymic = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    educational_institution = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref=db.backref('profile', uselist=False))

    def __repr__(self):
        return f"<profiles {self.id}>"


class Olympiad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    introduction = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<olympiad {self.id}>"

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_title = db.Column(db.String(100), nullable=True)
    institution_director = db.Column(db.String(100), nullable=True)
    institution_email = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Institution {self.id}>"

class Applications_for_addition_Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Applications_for_addition_Institution {self.id}>"

class Sent_applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_olympiad = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    surname = db.Column(db.String(50), nullable=True)
    patronymic = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    educational_institution = db.Column(db.String(100))
    classe = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(50), nullable=True)
    approved = db.Column(db.String(100), default="Заявка на рассмотрении")

    __table_args__ = (db.UniqueConstraint('title_olympiad', 'email', name='_title_email_uc'),)

    def __repr__(self):
        return f"<Sent_applications {self.id}>"

class Science_application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_olympiad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    purpose_project = db.Column(db.Text, nullable=False)
    project_tasks = db.Column(db.Text, nullable=False)
    product_purpose = db.Column(db.Text, nullable=False)
    scientific_novelty = db.Column(db.Text, nullable=False)
    rationale_conducting_research = db.Column(db.Text, nullable=False)
    main_technical_parameters = db.Column(db.Text, nullable=False)
    design_requirements = db.Column(db.Text, nullable=False)
    patent_requirements = db.Column(db.Text, nullable=False)
    application_area = db.Column(db.Text, nullable=False)
    volume_off_budget_investments = db.Column(db.Text, nullable=False)
    available_analogues = db.Column(db.Text, nullable=False)
    project_commercialization_plan = db.Column(db.Text, nullable=False)
    job_evaluation = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Science_application {self.id}>"