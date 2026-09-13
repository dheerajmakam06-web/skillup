from datetime import datetime

from app import db


class RoadmapProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_key = db.Column(db.String(128), nullable=False)
    module_key = db.Column(db.String(160), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_key', 'module_key', name='uq_roadmap_progress_course_module'),
    )

    def mark(self, completed):
        self.completed = completed
        self.completed_at = datetime.utcnow() if completed else None
