from flask import Blueprint, render_template
from website.model import Transaction, TransactionType
user_view = Blueprint('user_view', __name__)

@user_view.route('/')
def home():
	return render_template('home.html')

@user_view.route('/issues/')
def view_issues():
	all_issues = Transaction.query.filter_by(transaction_type = TransactionType.ISSUE).order_by(Transaction.transaction_date.desc()).all()
	return render_template("show-issues.html", issues = all_issues)

@user_view.route('/returns/')
def view_returns():
	all_returns = Transaction.query.filter_by(transaction_type = TransactionType.RETURN).order_by(Transaction.updated_on.desc()).all()
	return render_template("show-returns.html", returns = all_returns)