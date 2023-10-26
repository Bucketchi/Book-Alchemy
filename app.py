from flask import Flask, request, redirect, url_for, render_template
from data_models import db, Author, Book
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

db.init_app(app)


@app.route('/')
def home():
    sort_by = request.args.get('sort', 'title')

    # Define a default sorting function

    sort_function = func.lower(Book.title)

    if sort_by == 'author':
        sort_function = func.lower(Author.name)

    books = db.session.query(Book, Author.name).join(Author, Author.id == Book.author_id).order_by(sort_function).all()

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        author = Author(
            name=request.form['name'],
            birth_date=request.form['birthdate'],
            date_of_death=request.form['date_of_death']
        )

        db.session.add(author)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = Book(
            isbn=request.form['isbn'],
            title=request.form['title'],
            publication_year=request.form['publication_year'],
            author_id=request.form['id']
        )

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('home'))

    authors = Author.query.with_entities(Author.id, Author.name).all()

    return render_template('add_book.html', authors=authors)


@app.route('/search')
def search():
    search_term = request.args.get('s', '')

    books = db.session.query(Book, Author.name).join(Author, Author.id == Book.author_id).filter(
        Book.title.like(f"%{search_term}%")).all()

    error = ""

    if len(books) == 0:
        error = "No books match the search criteria"

    return render_template('home.html', books=books, message=error)


@app.route('/book/<int:book_id>/delete')
def delete(book_id):
    book_to_delete = db.session.query(Book).get(book_id)

    if book_to_delete:
        # Delete the book if it exists
        db.session.delete(book_to_delete)
        db.session.commit()

    books = db.session.query(Book, Author.name).join(Author, Author.id == Book.author_id).all()

    message = "Book successfully deleted"

    return render_template('home.html', books=books, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
