from flask_login import UserMixin


from __init__ import db, manager


class bot_user(db.Model):
    user_id = db.Column(db.String(128), primary_key = True)

class opk_aud(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)

class opk_group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_spec = db.Column(db.Integer, nullable=False)
    name_group = db.Column(db.String(31), nullable=False)
    srok = db.Column(db.Integer, nullable=False)

class opk_spec(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(127), nullable=False)
    nameSize = db.Column(db.String(15), nullable=False)

class admins_sait (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

class opk_sotr(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(127), nullable=False)

class time(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title_column = db.Column(db.String(128), nullable=False)
    hourUP_b = db.Column(db.Integer)
    minutUP_b = db.Column(db.Integer)
    hourEND_b = db.Column(db.Integer)
    minutEND_b = db.Column(db.Integer)
    hourUP_s = db.Column(db.Integer)
    minutUP_s = db.Column(db.Integer)
    hourEND_s = db.Column(db.Integer)
    minutEND_s = db.Column(db.Integer)

@manager.user_loader
def load_user(user_id):
    return admins_sait.query.get(user_id)
