import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from ..util.random import random_string


class Skill(SqlAlchemyBase, UserMixin):
    # Класс для хранения информации о навыке
    __tablename__ = 'skills'

    port = sqlalchemy.Column(sqlalchemy.Integer)
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    skill_name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    salt = sqlalchemy.Column(sqlalchemy.String)
    database_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
