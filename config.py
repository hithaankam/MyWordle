import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"