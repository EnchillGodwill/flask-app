from config import db


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    cal_volt = db.Column(db.Float, nullable=True)
    cal_conc = db.Column(db.Float, nullable=True)
    nit_volt = db.Column(db.Float, nullable=True)
    nit_conc = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Reading %r>' % self.created_at

    def __str__(self):
        return self.created_at


db.create_all()
db.session.commit()
