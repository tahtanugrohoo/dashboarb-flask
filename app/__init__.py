from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "admin.login"

    # register models agar terbaca Alembic
    from .models import admin_user, respondent, response, clustering, prediction  # noqa

    # register blueprints
    from .blueprints.public import public_bp
    from .blueprints.admin import admin_bp
    from .blueprints.analytics import analytics_bp
    from .blueprints.export import export_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")
    app.register_blueprint(export_bp, url_prefix="/export")

    return app
