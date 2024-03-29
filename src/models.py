import enum
from contextlib import contextmanager

from loguru import logger
from sqlalchemy import (Column, Enum, ForeignKey, Integer, String, Text,
                        create_engine)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    uploaded_htmls = relationship("RawHtml", back_populates="uploaded_by_user")

    @hybrid_property
    def empty_credentials(self):
        return (not self.login) or (not self.password)


class HtmlType(enum.Enum):
    summary = "summary"
    running_attempt = "running_attempt"
    finished_attempt = "finished_attempt"
    all_course_tasks = "all_course_tasks"
    all_courses = "all_courses"


class RawHtml(Base):
    __tablename__ = "raw_html"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False, comment="HTML content")
    origin = Column(Text, nullable=False, comment="Download URL")
    type = Column(Enum(HtmlType), nullable=False)
    uploaded_by_user_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    uploaded_by_user = relationship("User", back_populates="uploaded_htmls")


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
        except SQLAlchemyError as e:
            s.rollback()
            logger.error(f"Failed to execute SQL query with error {e}")
        finally:
            s.close()

    def first_seen(self, user_id: int) -> bool:
        return not self.get_user(user_id)

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def add_user(self, id: int, login: str = None, password: str = None) -> None:
        self.session.add(User(id=id, login=login, password=password))
        self.session.commit()

    def update_user(
        self, id: int, new_login: str = None, new_password: str = None
    ) -> bool:
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
            print(f"Failed to delete user {id} with error {e}")

    def safely_upload_html(
        self,
        origin_url: str,
        html_content: str,
        html_content_type: HtmlType,
        by_user: int = None,
    ):
        logger.info(f"Uploading HTML page from user={by_user} and origin={origin_url}")
        try:
            with self.safe_session() as session:
                session.add(
                    RawHtml(
                        content=html_content,
                        origin=origin_url,
                        type=html_content_type,
                        uploaded_by_user_id=by_user,
                    )
                )
        except Exception as e:
            logger.error(f"Unknown error {e}")
