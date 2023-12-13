from website import db
from website.model import Transaction, TransactionType

class TransactionDAO():

	def addTransaction(member_id, book_id, transaction_type, rent_paid = False):
		if transaction_type == 'issue':
			transaction_type = TransactionType.ISSUE
		else:
			transaction_type = TransactionType.RETURN

		new_transaction = Transaction(
			book_id = book_id,
			member_id = member_id,
			transaction_type = transaction_type,
			rent_paid = rent_paid
		)
		try:
			db.session.add(new_transaction)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			print(f"Error while adding transaction! {e}")
			raise 
	
	def updateTransaction(transaction, changes):

		for key, value in changes.items():
			if hasattr(transaction, key):
				setattr(transaction, key, value)
			else:
				print(f"Ignoring unknown attribute: {key}")	
		
		try:
			db.session.commit()
		except:
			db.session.rollback()
			print("Could not update transaction")
			raise
