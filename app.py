from website import create_app, create_initial_db

app = create_app()

with app.app_context():
    create_initial_db()

if __name__ == '__main__':
	app.run()

