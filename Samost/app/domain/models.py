from app import db, app

class ReviewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()