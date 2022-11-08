from config import db


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    meta_data = db.Column(db.String(300), nullable=True)
    value = db.Column(db.Float, nullable=True)
    device = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)


db.create_all()
db.session.commit()
