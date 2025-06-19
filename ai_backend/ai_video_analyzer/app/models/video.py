from app import db

class VideoAnalysis(db.Model):
    __tablename__ = 'video_analysis'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    flags = db.Column(db.JSON)
