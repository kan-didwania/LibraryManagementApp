import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SQLAlchemy()

def create_app():
	basedir = os.path.abspath(os.path.dirname(__file__))

	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] =\
			'sqlite:///' + os.path.join(basedir, 'database.db') 
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.secret_key = '#$ab9&^BB00_.'
	db.init_app(app)

	from .routes.books import books_view
	from .routes.members import members_view
	from .routes.user import user_view

	app.register_blueprint(books_view)
	app.register_blueprint(members_view)
	app.register_blueprint(user_view)

	with app.app_context():
		db.create_all()
		print("\n\n\nCreated Database!")

	return app

from website.init_db import create_initial_members

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_initial_db():
		create_initial_members()

