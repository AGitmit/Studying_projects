from database_config import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Posts(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    likes = db.Column(db.Integer, default=0)