from.app import app
from flask import render_template
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired
from flask import url_for, redirect
from wtforms import PasswordField
from .models import User
from hashlib import sha256
from flask_login import login_user , current_user, logout_user, AnonymousUserMixin, login_required
from flask import request
# print(data[0])

class AuthorForm ( FlaskForm ):
    id = HiddenField('id')
    name = StringField ('Nom ', validators =[ DataRequired ()])
@app.route("/")
def home():
    print(current_user)
    print(current_user.is_authenticated)
    return render_template("home.html",title="My Books!",books = get_sample(),current_user=current_user)
@app.route("/detail/<id>")
def detail(id):
    books = get_books()
    print(books)
    print(len(books))
    book = books[int(id)-1]
    print(book)
    return render_template(
        "detail.html",
        book=book)
@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
    "edit-author.html",
    author=a, form=f)
@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('home', id=a.id))
    a = get_author(int(f.id.data))
    return render_template(
    "edit-author.html",
    author=a, form=f)
@app.route("/new/author/")
def new_author():
    f= AuthorForm()
    return render_template("new-author.html" ,form=f)
@app.route("/create/author/", methods=("POST",))
def create_author():
    f = AuthorForm()
    if f.validate_on_submit():
        a = Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("new-author.html", form=f)
class LoginForm ( FlaskForm ):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None
@app.route("/login/", methods=("GET", "POST"))
def login():
    f = LoginForm()
    if not current_user.is_authenticated:
        f.next.data = request.args.get("next")
    else:
        return redirect(url_for("home"))
    user = None  # Initialisation de la variable user à None
    
    if f.validate_on_submit():
        user = f.get_authenticated_user()
    if user:  # S'assurer que user est bien défini et non None
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/books/")
def books():
    return render_template("books.html", books=get_books())
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query', '')
    books = get_recherche(query)
    return render_template('search_results.html', books=books,query=query)
class BookForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    img = StringField('Image', validators=[DataRequired()])
    author_id = StringField('Author', validators=[DataRequired()])
@app.route("/create/book/", methods=("POST",))
def create_book():
    f = BookForm()
    if f.validate_on_submit():
        b = Book(price=float(f.price.data),
        title=f.title.data,
        url=f.url.data,
        img=f.img.data,
        author_id=f.author_id.data)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("new-book.html", form=f)

@app.route('/new/book/')
def new_book():
    f = BookForm()
    return render_template("new-book.html", form=f)