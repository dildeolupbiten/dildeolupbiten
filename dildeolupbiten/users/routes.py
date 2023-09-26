# -*- coding: utf-8 -*-

import os

from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from flask import redirect, url_for, request, flash, render_template, Blueprint, json, Response

from dildeolupbiten.users.models import User
from dildeolupbiten import bcrypt, db, mail
from dildeolupbiten.utils import save_image, get_user_articles
from dildeolupbiten.users.forms import LoginForm, RegistrationForm, AccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.view"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.view"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            return redirect(url_for("users.login"))
    return render_template(
        "users/login.html",
        title="Login",
        form=form,
        columns=[form.email, form.password],
        names=["email", "password"]
    )


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.view"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template(
        "users/register.html",
        title="Register",
        form=form,
        columns=[form.username, form.email, form.password, form.confirm_password],
        names=["username", "email", "password", "confirm_password"]
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.view"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.image.data:
            current_user.image = save_image(form, request.files["image"], (50, 50))
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template(
        "users/account.html",
        title="Account",
        form=form,
        columns=[form.username, form.email, form.image],
        names=["username", "email", "image"]
    )


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.view"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        msg = Message("Password Reset Request", sender=os.environ["MAIL_USERNAME"], recipients=[user.email])
        msg.body = (
            f"To reset your password, visit the following link: "
            f"{url_for('users.reset_password', token=token, _external=True)}"
        )
        mail.send(msg)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template(
        "users/reset_request.html",
        title="Reset Request",
        form=form,
        columns=[form.email],
        names=["email"]
    )


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.view"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template(
        "users/reset_password.html",
        title="Reset Password",
        form=form,
        columns=[form.password, form.confirm_password],
        names=["password", "confirm_password"]
    )


@users.route("/user/<string:username>")
def view(username):
    user = User.query.filter_by(username=username).first_or_404()
    articles = get_user_articles(user)[:6]
    if "articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template("users/view.html", user=user, title=username, exists=len(articles))


@users.route("/user/<string:username>/all_articles", methods=["GET", "POST"])
def all_articles(username):
    user = User.query.filter_by(username=username).first_or_404()
    articles = get_user_articles(user)
    if "all_articles" in request.form:
        return Response(json.dumps(articles), 200)
    return render_template(
        'users/list.html',
        title=f"{username} - All Articles",
        user=user
    )


@users.route("/user/<string:username>/delete", methods=["GET"])
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash("User has been deleted.", "success")
    return redirect(url_for("main.view"))
