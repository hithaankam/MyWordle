from flask import Flask

from config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.game import game_bp
from routes.reports import reports_bp


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(reports_bp)

    @app.get("/")
    def index():
        return "Wordle Backend Running"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)