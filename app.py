from website import create_app, create_initial_db

app = create_app()

if __name__ == '__main__':

	with app.app_context():
		create_initial_db()

	app.run()

