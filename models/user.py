from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from blog.security import flask_bcrypt


class User(db.Model, UserMixin):
    email = Column(String(255), unique=True, nullable=False, default="", server_default="")
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    _password = Column(LargeBinary, nullable=True)
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)
    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)
