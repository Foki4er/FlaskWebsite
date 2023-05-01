from sqlalchemy.orm import Session
from Models.Users import UserPost
from user_data import db, Users, Profiles


class UserRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add(self, user: UserPost):
        try:
            user_db = Users(
                email=user.email
            )
            user_db.password = user.psw
            pofile_db = Profiles(
                name=user.pr.name,
                old=user.pr.old,
                city=user.pr.city
            )
            user_db.pr = pofile_db
            self.__session.add(user_db)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get_by_email(self, email: str) -> Users:
        return self.__session.query(Users).filter(Users.email == email).first()

    def update(self, user: Users):
        try:
            self.__session.add(user)
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, user: Users):
        try:
            self.__session.delete(user)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get(self, id_user: int) -> Users:
        return self.__session.get(Users, id_user)