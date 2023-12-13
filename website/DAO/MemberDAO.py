from website import db
from website.model import Member
from sqlalchemy.exc import IntegrityError

class MemberDAO():
		
	def showAllMembers():
		members = Member.query.all()
		return members
	
	def getMemberById(member_id):
		member = Member.query.get(member_id)
		return member

	def deleteMember(member):
		try:
			db.session.delete(member)
			db.session.commit()
		except:
			db.session.rollback()
			print(f"Error while deleting member: {member.member_id}")
	
	