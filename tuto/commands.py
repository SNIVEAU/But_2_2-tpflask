import click
from .app import app, db
@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    # Creates the tables and populates them with data.'
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    import yaml
    books = yaml.safe_load(open(filename))
    # import des modèles
    from .models import Author, Book, User
    from hashlib import sha256

    # première passe: création de tous les auteurs
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            print(a)
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
            db.session.commit()
    # deuxième passe: création de tous les livres
    for b in books:
        a = authors[b["author"]]
        o = Book(price = b["price"],
        title = b["title"],
        url = b["url"] ,
        img = b["img"] ,
        author_id = a.id)
        db.session.add(o)
    m=sha256()
    m.update("test".encode('utf-8'))
    useradmin = User(username="test", password=m.hexdigest(), admin=True)
    db.session.add(useradmin)
    db.session.commit()
@app.cli.command()
def syncdb():
    db.drop_all()
    db.create_all()
    db.session.commit()
@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    from .models import User
    from hashlib import sha256
    m=sha256()
    m.update(password.encode('utf-8'))
    u=User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()
@app.cli.command()
def passwd(username, password):
    from .models import User
    u = User.query.filter_by(username=username).first()
    from hashlib import sha256
    m=sha256()
    m.update(password.encode('utf-8'))
    u.password = m.hexdigest()
    db.session.commit()

