import subprocess
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from configurator.data.db_session import SqlAlchemyBase


class Machine(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'machines'
    port = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    process = None

    def start(self):
        if self.process is not None:
            raise RuntimeError("Machine is already running!")
        self.process = subprocess.Popen(["python3", "../executor.py", f"{self.port}"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

    def stop(self):
        self.process.terminate()
        self.process = None

    def is_running(self):
        return self.process.poll() is None
