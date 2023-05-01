from flask import redirect, render_template, request, url_for, flash
from user_data import db
from Repositores import OlympiadRepository
from Models.Olympiada import PostOlympiad


class Generate_something:
    def __init__(self):
        self.__olympiad_repository: OlympiadRepository = OlympiadRepository(db.session)

    def generate_olympiad(self):
        if request.method == 'POST':

            olympiad = PostOlympiad(**request.form)

            self.__olympiad_repository.add(olympiad)

            return redirect('/admin/сompetitions')

        return render_template('admin/create-article.html')