import requests
from website.DAO.BookDAO import *
from website.DAO.MemberDAO import *
from website.DAO.TransactionDAO import *
from website.model import Books
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
import datetime

def importBooks(payload, number_of_books):
	flashes = []
	
	response_data = {}
	try:
		response_data = requests.post('https://frappe.io/api/method/frappe-library', params = payload).json()
	except:
		print("Error while fetching data")
		raise

	if "message" not in response_data:
		print("Error while fetching data")
		return ["Could not fetch data from API"]

	for book_data in response_data["message"]:
		book_id = int(book_data["bookID"])
		book = BookDAO.getBookById(book_id)
		if book:
			copies = book.quantity
			copies += number_of_books
			updateBook(book, {"quantity": copies})
			continue
		try:
			addBook(book_data, number_of_books)
		except:
			flashes.append(f'Could not add Book {book_data["title"]}')
	try:
		db.session.commit()
	except:
		raise
		

def addBook(book_data, number_of_books):

	new_book = Books(
		id = int(book_data["bookID"]),
		title = book_data["title"],
		authors = book_data["authors"],
		isbn = book_data["isbn"],
		isbn13 = book_data["isbn13"],
		language_code = book_data["language_code"],
		ratings_count = int(book_data["ratings_count"]),
		num_pages = int(book_data["  num_pages"]),
		text_reviews_count = int(book_data["text_reviews_count"]),
		average_rating = Decimal(book_data["average_rating"]),
		quantity = number_of_books,
		publication_date = datetime.datetime.strptime(book_data["publication_date"], '%m/%d/%Y').date(),
		publisher = book_data["publisher"]
	)
	try:
		db.session.add(new_book)
	except IntegrityError as e:
		raise e

def searchBooks(params):
    if len(params) == 1:
        if "id" in params:
            return BookDAO.getBookById(params["id"])
		
    conditions = build_query_conditions(params)
    books = BookDAO.getBooksByConditions(conditions)
    
    return books
		
def issueBook(book_id, member_id):
	member = MemberDAO.getMemberById(member_id)
	if not member:
		return [False, "Member not found!"]
	
	if member.rent_due >= 500:
		print("Rent Overdue! Cannot issue book.")
		return [False, "Member's rent is Overdue! Cannot issue book"]
	
	book = BookDAO.getBookById(book_id)
	if not book:
		return [False, "Book not found!"]
	
	if book.quantity <= 0:
		print("Book out of stock!")
		return [False, "Book out of stock!"]
	
	try:
		copies = book.quantity
		copies -= 1
		updateBook(book, {"quantity": copies})
		TransactionDAO.addTransaction(member_id, book_id, 'issue')
	except Exception as e:
		print(f"Error while issuing book! {e}")
		raise
	return [True, "Book issued successfully!"]
	
def build_query_conditions(params):
	conditions = []
	for key, value in params.items():
		if key in ["authors", "title"]:
			conditions.append(getattr(Books, key).ilike(f'%{value}%'))
		else:
			conditions.append(getattr(Books, key) == value)
	return conditions
	
def getBorrowers(book_id):
		book = BookDAO.getBookById(book_id)
		if book is None:
			return []  
		
		borrowers = []
		book_transactions = book.transactions
		for transaction in book_transactions:
			if transaction.transaction_type == TransactionType.ISSUE:
				if transaction.borrower is None:
					continue
				borrowers.append(transaction.borrower)
		return borrowers

def editBookDetails(book_id, changes):
	book = BookDAO.getBookById(book_id)
	updateBook(book, changes)
	try:
		db.session.commit()
	except:
		db.session.rollback()
		print("Error editing Book Details!")
		raise

def updateBook(book, changes):
	
	for key, value in changes.items():
		if hasattr(book, key):
			setattr(book, key, value)
		else:
			print(f"Ignoring unknown attribute: {key}")	
	return book