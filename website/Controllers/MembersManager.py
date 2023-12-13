from website.DAO.MemberDAO import *
from website.DAO.BookDAO import *
from website.DAO.TransactionDAO import *
from website.Controllers.BooksManager import updateBook
from website.model import Member
from datetime import datetime
from decimal import Decimal

def addMember(params):
	new_member = Member(
		first_name = params['first_name'],
		last_name = params['last_name'],
		contact_no = params['contact_no'],
		adress = params['adress'],
		rent_charged = params['rent_charged'],
		rent_due = 0
	)

	try:
		db.session.add(new_member)
		db.session.commit()
	except IntegrityError as e:
		db.session.rollback()
		print(f"Error inserting data: {e}")
		raise


def searchMember(params):
	if len(params) == 1:
		if "id" in params:
			member = MemberDAO.getMemberById(params["id"])
			return member
		
def getIssuedBooks(member_id):
		member = MemberDAO.getMemberById(member_id)
		if member is None:
			return []
		books_issued = []
		member_transactions = member.transactions
		for transaction in member_transactions:
			if transaction.transaction_type == TransactionType.ISSUE:
				if transaction.borrowed_book is None:
					continue
				books_issued.append(transaction.borrowed_book)
		return books_issued

def deleteMember(member_id):
	member = MemberDAO.getMemberById(member_id)
	if member is None:
		return "Member Not found!"
	
	member_transactions = member.transactions
	for transaction in member_transactions:
		if transaction.transaction_type == TransactionType.ISSUE:
			if transaction.borrowed_book is None:
				continue
			book_to_be_updated = transaction.borrowed_book
			copies = book_to_be_updated.quantity
			copies += 1
			updateBook(book_to_be_updated, {"quantity": copies})
	try:
		MemberDAO.deleteMember(member)
		return "Member deleted successfully. "
	except:
		return "Could not delete member!"

def updateMember(member, changes):

	for key, value in changes.items():
		if hasattr(member, key):
			setattr(member, key, value)
		else:
			print(f"Ignoring unknown attribute: {key}")	
	return member

def returnBook(member_id, book_id, rent_paid):
	
	member = MemberDAO.getMemberById(member_id)
	if member is None:
		print("No such member found!")
		return "Member not found!"
	book = BookDAO.getBookById(book_id)
	if book is None:
		print("No such book found!")
		return "Book not found!"
	
	#See the initial Issue transaction and change the status from ISSUE to RETURN
	issue_transaction = Transaction.query.filter_by(
		book_id = book_id, 
		member_id = member_id, 
		transaction_type = TransactionType.ISSUE).first()
	
	if issue_transaction is None:
		return "The member did not issue this book"
	
	#increase number of copies in the database
	copies = book.quantity
	copies += 1
	updateBook(book, {"quantity": copies})
	
	changes = {
		"transaction_type": TransactionType.RETURN,
		"updated_on": datetime.now()
	}

	# Check whether the member has paid the rent or it has to be added in due
	if rent_paid == member.rent_charged:
		changes["rent_paid"] = True
	else:
		rent_to_be_paid = member.rent_charged - rent_paid
		rent_due = rent_to_be_paid + member.rent_due
		updateMember(member, {"rent_due": rent_due})

	try:
		TransactionDAO.updateTransaction(issue_transaction, changes)
		return "Book returned."
	except:
		print("Could not return the book.")
		return "Could not return the book!"

def editMemberDetails(member_id, changes):
	member = MemberDAO.getMemberById(member_id)
	updateMember(member, changes)
	try:
		db.session.commit()
	except:
		db.session.rollback()
		print("Error while updating member!")
		raise

	


