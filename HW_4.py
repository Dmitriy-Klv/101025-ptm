from app.extensions import db
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

# 1 все наследуются от db.Model
# 2 у всех есть ОДНО И ТО ЖЕ поле id
# 3 у всех есть ОДНА И ТА ЖЕ НАСТРОЙКА __tablename__


class Model(db.Model):
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr.directive
    def id(cls):
        return db.Column(
            db.Integer,
            primary_key=True,
            autoincrement=True
        )


# SQLAlchemy v1 format
class Category(Model):
    name = db.Column(db.String(100), nullable=False)

    questions = db.relationship('Question', backref='category', lazy=True)

    def __repr__(self):
        return f'Category: {self.name}'



var = 5
var: int = 5

# SQLAlchemy v2 format
class Category(Model):

    # Mapped[str] сторона объектов питона
    # mapped_column сторона объектов ORM системы для базы данных
    name: Mapped[str] = mapped_column(
        db.String(100),
        nullable=False
    )

    questions = db.relationship('Question', backref='category', lazy=True)


class Question(Model):
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)


    responses = db.relationship('Response', backref='question', lazy=True)

    def __repr__(self):
        return f'Question: {self.text}'


class Statistic(Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        # return '<Statistic for Question %r: %r agree, %r disagree>' % (self.question_id, self.agree_count,
        return f'<Statistic for Question {self.question_id}: {self.agree_count} agree, {self.disagree_count} disagree>'