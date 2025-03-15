from flask import Flask
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_NAME = "product_inventory.db"
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # migrate = Migrate(app, db) # In case changes happen in models.py

    from .model import Product
    if not path.exists("../instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app