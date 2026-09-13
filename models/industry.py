from app import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    industry = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128))
    description = db.Column(db.Text)
    category = db.Column(db.String(32), default='established')
    rating = db.Column(db.Float, default=4.0)
    opportunity_type = db.Column(db.String(32), default='employment')
    course_tags = db.Column(db.String(256))
    official_url = db.Column(db.String(512))
    demands = db.relationship('IndustryDemand', backref='company', cascade='all, delete-orphan')


class IndustryDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    skill_name = db.Column(db.String(128), nullable=False)
    importance = db.Column(db.String(32), default='required')
