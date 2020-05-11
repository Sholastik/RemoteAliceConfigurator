from sqlalchemy_serializer import SerializerMixin
import sqlalchemy

from runner.data.db_session import SqlAlchemyBase


class Command(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'commands'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    action_name = sqlalchemy.Column(sqlalchemy.String)
    trigger = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    port = sqlalchemy.Column(sqlalchemy.Integer, index=True)
