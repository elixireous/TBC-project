from ext import app, db
from models import User

with app.app_context():
    admin_user = User("Ilia", "iliasakvarelidze7@gmail.com", "test1234", "admin")
    db.session.add(admin_user)
    db.create_all()
    db.session.commit()
