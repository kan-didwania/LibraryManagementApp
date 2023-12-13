from . import db
from sqlalchemy.sql import func
from enum import Enum

class TransactionType(Enum):
    ISSUE = 'issue'
    RETURN = 'return'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column( db.Integer, db.ForeignKey('books.id', ondelete = 'CASCADE'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id', ondelete = 'CASCADE'))
    transaction_type = db.Column(db.Enum(TransactionType), nullable = False)
    transaction_date = db.Column(db.DateTime(timezone = True), default = func.now())
    updated_on = db.Column(db.DateTime(timezone = True))
    rent_paid = db.Column(db.Boolean, nullable=False)
    
class Books(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   authors = db.Column(db.String(100))
   isbn = db.Column(db.String(10), nullable=False)
   isbn13 = db.Column(db.String(13), nullable=False)
   language_code = db.Column(db.String(3), nullable=True)
   ratings_count = db.Column(db.Integer)
   num_pages = db.Column(db.Integer)
   text_reviews_count = db.Column(db.Integer)
   average_rating = db.Column(db.Numeric(4, 2))
   quantity = db.Column(db.Integer, default = 1)
   publication_date = db.Column(db.Date)
   publisher = db.Column(db.String(100))
   transactions = db.relationship('Transaction', backref='borrowed_book', cascade='all, delete-orphan', passive_deletes=True)
	
class Member(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(30), nullable=False)
   last_name = db.Column(db.String(30), nullable=True)
   adress = db.Column(db.String(50), nullable=False)
   contact_no = db.Column(db.String(10), nullable=False, unique=True)
   rent_charged = db.Column(db.Numeric(scale = 2))
   rent_due = db.Column(db.Numeric(scale = 2), default = 0)
   transactions = db.relationship('Transaction', backref = 'borrower', cascade='all, delete-orphan', passive_deletes=True)