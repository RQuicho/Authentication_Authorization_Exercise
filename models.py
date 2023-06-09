from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app_):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, primary_key=True, length=20)
    password = db.Column(db.Test, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True, length=50)
    first_name = db.Column(db.String, nullable=False, length=30)
    last_name = db.Column(db.String, nullable=False, length=30)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/ hashed password & return user"""

        hashed = bcryp.generate_password_hash(pwd)
        hashed_utf8 = hahsed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd, email, first_name, last_name):
        """Validate that user exists & password is correct"""

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False