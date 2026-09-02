import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # print("DATABASE_URL =", os.environ.get("DATABASE_URI"))

    # SQLALCHEMY_DATABASE_URI='sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

   