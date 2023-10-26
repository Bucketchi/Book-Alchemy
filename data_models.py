from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __str__(self):
        return f"Author:{self.name}, born {self.birth_date}"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id", ondelete="CASCADE"))

    def __str__(self):
        return f"Book: {self.title}, published in {self.publication_year}"
