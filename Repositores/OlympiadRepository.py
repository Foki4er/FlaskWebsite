from sqlalchemy.orm.session import Session
from user_data import Olympiad
from Models.Olympiada import PostOlympiad


class OlympiadRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add(self, olympiad: PostOlympiad):
        try:
            olympiad = Olympiad(**olympiad.dict())
            self.__session.add(olympiad)
            self.__session.commit()
        except:
            self.__session.rollback()

