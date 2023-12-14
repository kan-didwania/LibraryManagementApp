from flask import Blueprint, flash
from flask import  render_template, request, url_for, redirect
from website.Controllers.BooksManager import *
from website.DAO.BookDAO import *

books_view = Blueprint('books_view', __name__)

@books_view.route('/books/', methods = ['GET', 'POST'])
def import_books():
	if request.method == 'POST':

		if request.form.get('quantity'):
			number_of_books = int(request.form.get('quantity'))
		else:
			number_of_books = 1

		if number_of_books < 0:
			flash('Number of books cannot be negative. Enter a positive number')
			return redirect(url_for('books_view.import_books'))
			
		title = request.form.get('title')
		authors = request.form.get('authors')
		isbn = request.form.get('isbn')
		publisher = request.form.get('publisher')
		page = request.form.get('page')
		
		payload = {}
		if title:
			payload["title"] = title
		if authors:
			payload["authors"] = authors
		if isbn:
			payload["isbn"] = isbn
		if publisher:
			payload["publisher"] = publisher
		if page:
			payload["pages"] = page
		try:
			flashes = importBooks(payload, number_of_books)
			if flashes is not None:
				flash(flashes)
			else:
				flash('Books imported successfully!')
		except:
			flash("Could not import books!")
		redirect(url_for('books_view.import_books'))

	return render_template('import-books.html')

@books_view.route('/books/show', methods = ['GET'])
def show_all_books():
	books = BookDAO.getAllBooks()
	return render_template('show-books.html', books = books)

@books_view.route('/books/<int:book_id>')
def book_details(book_id):
	book = searchBooks({"id": book_id})
	return render_template('book-details.html', book = book)

@books_view.route('/books/edit/<int:id>', methods = ['GET', 'POST'])
def edit_book(id):
	if request.method == 'POST':
		changes = {}
		changes["quantity"] = int(request.form.get('quantity'))
		changes["title"] = request.form.get('title')
		changes["authors"] = request.form.get('authors')
		changes["isbn"] = request.form.get('isbn')
		changes["isbn13"] = request.form.get('isbn13')
		changes["publisher"] = request.form.get('publisher')
		changes["num_pages"] = int(request.form.get('num_pages'))
		changes["language_code"] = request.form.get('language_code')
		changes["ratings_count"] = int(request.form.get('ratings_count'))
		changes["text_reviews_count"] = int(request.form.get('text_reviews_count'))
		changes["average_rating"] = Decimal(request.form.get('average_rating'))
		publication_date = datetime.datetime.strptime(request.form.get('publication_date'), '%Y-%m-%d').date().strftime('%m/%d/%Y')
		changes["publication_date"] = datetime.datetime.strptime(publication_date, '%m/%d/%Y')

		if len(changes['isbn']) != 10 or len(changes['isbn13']) != 13:
			flash('Wrong ISBN')
			redirection = True
		
		try:
			editBookDetails(id, changes)
			flash('Book details edited successfully!')
		except:
			flash('Could not edit details!')
		return redirect(url_for('books_view.book_details', book_id = id))

	book = searchBooks({"id": id})
	return render_template("edit-book.html", book=book)

@books_view.route('/books/issue/<int:id>', methods = ['GET', 'POST'])
def issue_book(id):
	if request.method == 'POST':
		member_id = request.form.get('member_id')
		try:
			resp = issueBook(id, member_id)
			flash(resp[1])
		except:
			flash('Error while issuing book!')
		return redirect(url_for('books_view.book_details', book_id = id))
	else:
		book = searchBooks({"id": id})
		return render_template("issue-book.html", book=book)
	
@books_view.route('/books/delete/<int:id>')
def delete_book(id):
	try:
		BookDAO.deleteBook(id)
		flash('Book deleted.')
	except:
		flash("Could not delete book!")
		return redirect(url_for('books_view.book_details', book_id = id))
	
	return redirect(url_for('books_view.show_all_books'))

@books_view.route('/books/search/', methods = ['GET', 'POST'])
def search_book():
	if request.method == 'POST':
		book_title = request.form.get('title')
		authors = request.form.get('authors')
		params = {}
		if book_title:
			params["title"] = book_title
		if authors:
			params["authors"] = authors
		books = searchBooks(params)
		return render_template('show-books.html', books=books)
	return render_template('search-books.html')
	
@books_view.route('/books/borrowers/<int:id>')
def show_borrowers(id):
	borrowers = getBorrowers(id)
	return render_template("show-members.html", members = borrowers)