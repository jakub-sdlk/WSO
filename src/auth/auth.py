from flask import Blueprint, redirect, url_for, render_template, request, session, flash, get_flashed_messages
from src.db import db
from src.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


def show_correct_response_code(render_template_file):
    messages = get_flashed_messages(with_categories=True)
    error_during_login_flag = False
    for category, message in messages:
        if category == 'error':
            error_during_login_flag = True
    if error_during_login_flag:
        return render_template(render_template_file), 401
    return render_template(render_template_file), 200


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("login_email")
        password = request.form.get("login_password")

        user = User.find_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                if not'active_schedule_id' in session:
                    session['active_schedule_id'] = 1
                return redirect(url_for('stats.overview', schedule_selector=session['active_schedule_id']))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist", category='error')

    return show_correct_response_code("login.html")


# noinspection PyArgumentList
@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("signup_first_name")
        last_name = request.form.get("signup_last_name")
        email = request.form.get("signup_email")
        password = request.form.get("signup_password")

        email_exist = User.find_by_email(email)

        if email_exist:
            flash("This email is already registered.", category='error')
        elif not first_name:
            flash("First name is required.", category='error')
        elif not last_name:
            flash("Last name is required.", category='error')
        # Change this later for regex, or check the email_validator package
        elif len(email) < 5:
            flash("Email is invalid.", category='error')
        # Change this later for regex
        elif len(password) < 4:
            flash("Invalid password.", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method='sha256'))

            new_user.save_to_db()
            login_user(new_user, remember=True)
            flash('User created', category='success')
            return redirect(url_for('stats.overview', schedule_selector=1))

    return show_correct_response_code("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
