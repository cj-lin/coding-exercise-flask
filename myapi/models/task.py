from myapi.extensions import db


class Task(db.Model):
    """Basic task model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Task %s>" % self.name
