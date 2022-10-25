from app import db


class Save(db.Model):
    __tablename__ = 'saved_places'
    id = db.Column(db.Integer, primary_key=True)
    w_uuid = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    save_name = db.Column(db.String, nullable=False)
    save_url = db.Column(db.String, nullable=False)