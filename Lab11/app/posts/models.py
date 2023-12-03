from ..extensions import db
from enum import Enum


class TypeEnum(Enum):
    PUBLICATION = "Publication"
    NEWS = "News"
    OTHER = "Other"


post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post_model.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag_model.id')))


class TagModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'#{self.name} '


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)


class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(226), nullable=False)
    text = db.Column(db.String(226), nullable=True)
    image = db.Column(db.String(226), nullable=False, default="/defauly.jpg")
    created = db.Column(db.DateTime, nullable=False)
    post_type = db.Column(db.Enum(TypeEnum), nullable=False, default=TypeEnum.PUBLICATION)
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'), nullable=False, default=1)
    tags = db.relationship('TagModel', secondary=post_tag, backref='posts')

    def __repr__(self) -> str:
        return f"({self.title}, {self.text[:15]}..., {self.user_id})"
