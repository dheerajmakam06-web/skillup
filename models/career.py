from app import db

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    skills = db.relationship('CareerSkill', backref='career')

class CareerSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('career.id'))
    skill_name = db.Column(db.String(128))
    weight = db.Column(db.Float, default=1.0)
    importance = db.Column(db.String(32), default='medium')
