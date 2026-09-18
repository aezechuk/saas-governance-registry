import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    from config import config_by_name

    app.config.from_object(config_by_name[config_name])

    # Ensure the instance folder exists (holds the SQLite file in dev)
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.applications import applications_bp

    app.register_blueprint(applications_bp)

    return app
