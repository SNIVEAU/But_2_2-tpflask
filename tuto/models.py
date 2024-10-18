import yaml, os.path
from .app import db, login_manager
from flask_login import UserMixin
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __repr__(self):
        return self.name
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return "<Genre (%d) %s>" % (self.id, self.name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)


class Appartient(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    
    book = db.relationship(Book, backref=db.backref('genres', lazy='dynamic'))
    genre = db.relationship(Genre, backref=db.backref('books', lazy='dynamic'))

    def __init__(self, book_id, genre_id):
        self.book_id = book_id
        self.genre_id = genre_id

    def __repr__(self):
        return "<Appartient: Book %d, Genre %d>" % (self.book_id, self.genre_id)
    def get_genre_by_books(book_id):
        return Appartient.query.filter_by(book_id=book_id).all()
def get_sample():
    return Book.query.limit(10).all()
def get_author(id):
    return Author.query.get(id)
def get_books():
    return Book.query.all()
def get_recherche(query):
    return Book.query.filter(Book.title.like('%'+query+'%')).all()

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = password
        self.admin = admin
        
    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return True  



@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
