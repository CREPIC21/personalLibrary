from flask import Flask, render_template, request, redirect, url_for
# first it needs to be installed in terminal "pip install Flask-SQLAlchemy"
from flask_sqlalchemy import SQLAlchemy
import os

# creating the application
app = Flask(__name__)
# your database URI that should be used for the connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'your database URI'
# if set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# creating SQLAlchemy object by passing it the application
db = SQLAlchemy(app)

# Creating a new table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # This function will allow each book object to be identified by it's title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

# creating our database - once run needs to be commented as the database will be created
#db.create_all()

# home route where all the books will be displayed on the screen - book name, author, rating
@app.route('/')
def home():
    # getting all books that were added to our database
    all_books = Book.query.all()
    return render_template('index.html', library=all_books)

# "edit" route where we can change/update the rating of our existing books in database
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # getting the book from the database by their 'id' which we got when clicking on the "edit rating" button on our
    # home page and passing that id as argument to our edit function
    book_to_edit = Book.query.filter_by(id=id).first()
    if request.method == 'POST':
        new_rating = request.form['new_rating']
        book_to_edit.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book_to_edit)

# "delete" route where we can delete book from our database
@app.route('/delete/<int:id>')
def delete(id):
    # getting the book from the database by their 'id' which we got when clicking on the "delete" button on our
    # home page and passing that id as argument to our delete function
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# "add" route where we can add new book to our database
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_data = {
            "book_name": request.form['book_name'],
            "book_author": request.form['book_author'],
            "book_rating": request.form['book_rating'],
        }
        # all_books.append(book_data)
        new_book = Book(title=book_data['book_name'], author=book_data['book_author'], rating=book_data['book_rating'])
        db.session.add(new_book)
        db.session.commit()
        print(book_data)
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


