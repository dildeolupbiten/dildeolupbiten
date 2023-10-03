# -*- coding: utf-8 -*-

import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    DEBUG = False
    PORT = 5000
    BASIC_AUTH_USERNAME = os.environ["BASIC_AUTH_USERNAME"]
    BASIC_AUTH_PASSWORD = os.environ["BASIC_AUTH_PASSWORD"]
