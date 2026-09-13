from app import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)

class StudentSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    level = db.Column(db.Integer, default=0)  # 0-5
    verified = db.Column(db.Boolean, default=False)
    skill = db.relationship('Skill')
