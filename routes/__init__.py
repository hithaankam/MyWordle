from .auth import auth_bp
from .dashboard import dashboard_bp
from .game import game_bp
from .reports import reports_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "game_bp",
    "reports_bp",
]