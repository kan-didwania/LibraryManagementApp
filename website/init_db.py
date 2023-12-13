from .model import Member, db

def create_initial_members():
    members_data = [
		{
			"first_name": "John",
			"last_name": "Doe",
			"adress": "123 Main St",
			"contact_no": "1234567890",
			"rent_charged": 100
		},
		{
			"first_name": "Jane",
			"last_name": "Smith",
			"adress": "456 Oak St",
			"contact_no": "9876543210",
			"rent_charged": 100
		},
		{
			"first_name": "Alice",
			"last_name": "Johnson",
			"adress": "789 Pine St",
			"contact_no": "5551234567",
			"rent_charged": 50
		},
		{
			"first_name": "Bob",
			"last_name": "Williams",
			"adress": "321 Cedar St",
			"contact_no": "7890123456",
			"rent_charged": 100
		},
		{
			"first_name": "Eva",
			"last_name": "Davis",
			"adress": "567 Elm St",
			"contact_no": "3334445555",
			"rent_charged": 50
		}
	]

    for member_data in members_data:
        new_member = Member(**member_data)
        db.session.add(new_member)

    db.session.commit()
    print("Members added.")

