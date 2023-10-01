# -*- coding: utf-8 -*-

from os import environ
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView


class ViewModel(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == environ["BASIC_AUTH_USERNAME"]
