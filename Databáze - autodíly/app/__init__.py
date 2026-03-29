import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import get_config

db = SQLAlchemy()

# Cesty k šablonám a statickým souborům uvnitř balíčku app/
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(_APP_DIR, "static")
TEMPLATE_FOLDER = os.path.join(_APP_DIR, "templates")


def create_app():
    app = Flask(
        __name__,
        static_folder=STATIC_FOLDER,
        template_folder=TEMPLATE_FOLDER,
    )
    app.config.from_object(get_config())

    db.init_app(app)

    from . import models  # noqa: F401
    from .routes import main_bp

    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found(e):
        return (
            render_template(
                "error.html",
                code=404,
                title="Stránka nenalezena",
                message="Požadovaná stránka neexistuje. Zkontrolujte odkaz nebo se vraťte na přehled.",
            ),
            404,
        )

    @app.errorhandler(500)
    def server_error(e):
        return (
            render_template(
                "error.html",
                code=500,
                title="Chyba serveru",
                message="Došlo k vnitřní chybě. Zkuste to později nebo se vraťte na hlavní stránku.",
            ),
            500,
        )

    return app