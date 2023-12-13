from flask import Blueprint, render_template, request, url_for, redirect, flash
from website.DAO.MemberDAO import *
from website.Controllers.MembersManager import *

members_view = Blueprint('members_view', __name__)

@members_view.route('/members/', methods = ['GET', 'POST'])
def add_member():
	if request.method == 'POST':
		params = {}
		params['first_name'] = request.form.get('first_name')
		params['last_name'] = request.form.get('last_name')
		params['adress'] = request.form.get('adress')
		params['contact_no'] = request.form.get('contact_no')
		params['rent_charged'] = request.form.get('rent_charged')
		try:
			addMember(params)
			flash('Member added successfully!')
		except:
			flash('Could not add member!')
		return redirect(url_for('members_view.add_member'))
		
	return render_template('add-member.html')

@members_view.route('/members/show/', methods = ['GET'])
def show_all_members():
	members = MemberDAO.showAllMembers()
	return render_template('show-members.html', members = members)

@members_view.route('/members/<int:member_id>')
def member_details(member_id):
	member = searchMember({"id": member_id})
	return render_template('member-details.html', member = member)

@members_view.route('/members/edit/<int:id>', methods = ['GET', 'POST'])
def edit_member(id):
	if request.method == 'POST':
		changes = {}
		changes["first_name"] = request.form.get('first_name')
		changes["last_name"] = request.form.get('last_name')
		changes["contact_no"] = request.form.get('contact_no')
		changes["adress"] = request.form.get('adress')
		changes["rent_charged"] = request.form.get('rent_charged')
		changes["rent_due"] = request.form.get('rent_due')
		try:
			editMemberDetails(id, changes)
			flash('Member details edited.')
		except:
			flash('Could not edit details!')
		return redirect(url_for('members_view.member_details', member_id = id))

	member = searchMember({"id": id})
	return render_template("edit-member.html", member=member)

@members_view.route('/members/delete/<int:id>')
def delete_member(id):
	flash_message = deleteMember(id)
	flash(flash_message)
	return redirect(url_for('members_view.show_all_members'))

@members_view.route('/members/books_issued/<int:id>')
def show_books_issued(id):
	books_issued = getIssuedBooks(id)
	return render_template("show-books.html", books = books_issued)

@members_view.route('/members/return_book/<int:member_id>', methods = ['POST', 'GET'])
def return_book(member_id):
	if request.method == 'POST':
		book_id = int(request.form.get('book_id'))
		rent_paid = Decimal(request.form.get('rent_paid'))
		flash_message = returnBook(member_id, book_id, rent_paid)
		flash(flash_message)
		return redirect(url_for('members_view.member_details', member_id = member_id))
	member = MemberDAO.getMemberById(member_id)
	return render_template("return-book.html", member = member) if member is not None else redirect('/')


