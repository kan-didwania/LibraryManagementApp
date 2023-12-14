from website.model import Books
from website import db

class BookDAO():
	
	def getAllBooks():
		books = Books.query.all()
		return books
	
	def getBookById(book_id):
		book = Books.query.get(book_id)
		return book
	
	def getBooksByConditions(condtitions):
		books = Books.query.filter(*condtitions).all()
		return books

	def deleteBook(book_id):
		book = BookDAO.getBookById(book_id)

		try:
			db.session.delete(book)
			db.session.commit()
		except:
			db.session.rollback()
			print(f"Error while deleting book: {book_id}")
			raise

	


