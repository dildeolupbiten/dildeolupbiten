# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField


class Form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = StringField("Image", validators=[DataRequired()])


class ArticleForm(Form):
    submit = SubmitField("Create")


class ArticleUpdateForm(Form):
    submit = SubmitField("Update")
