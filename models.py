from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Tea(db.Model):
    __tablename__ = 'teas'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=1)

    def __init__(self, name, description, price, category, image_url=None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tea_id = db.Column(db.Integer, db.ForeignKey('teas.id'), nullable=False)  # Reference to 'teas'

    # Unique constraint for user and tea pair
    __table_args__ = (db.UniqueConstraint('user_id', 'tea_id', name='unique_user_tea_like'),)

    user = db.relationship('User', backref=db.backref('likes', lazy='dynamic'))
    tea = db.relationship('Tea', backref=db.backref('likes_by_users', lazy='dynamic'))

    def __repr__(self):
        return f"<Like(user_id={self.user_id}, tea_id={self.tea_id})>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
