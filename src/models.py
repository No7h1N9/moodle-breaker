from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    @hybrid_property
    def empty_credentials(self):
        return (not self.login) or (not self.password)


class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.session = Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

    @contextmanager
    def safe_session(self):
        s = Session(bind=self.engine)
        yield s
        try:
            s.commit()
        except SQLAlchemyError:
            s.rollback()
        finally:
            s.close()

    def first_seen(self, user_id: int) -> bool:
        return not self.get_user(user_id)

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def add_user(self, id: int, login: str = None, password: str = None) -> None:
        self.session.add(User(id=id, login=login, password=password))
        self.session.commit()

    def update_user(self, id: int, new_login: str=None, new_password: str=None) -> bool:
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            return False
        user.login, user.password = new_login, new_password
        self.session.commit()
        return True

    def delete_user(self, id: int):
        try:
            self.session.delete(User(id=id))
            self.session.commit()
        except Exception as e:
            print(f'Failed to delete user {id} with error {e}')
