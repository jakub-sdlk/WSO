from flask import Blueprint, redirect, url_for, render_template, request, session, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from redmail import gmail
import jwt

from models import User
from config import SECRET_KEY
from auth.templates.email_templates import VERIFICATION_TEMPLATE

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


def render_template_correct_status_code(render_template_file, **kwargs):
    messages = get_flashed_messages(with_categories=True)
    error_during_login_flag = False
    for category, message in messages:
        if category == 'error':
            error_during_login_flag = True
    if error_during_login_flag:
        return render_template(render_template_file), 401
    return render_template(render_template_file, **kwargs), 200


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("login_email")
        password = request.form.get("login_password")

        user = User.find_by_email(email)
        if user:
            if user.is_verified:
                if check_password_hash(user.password, password):
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    if not 'active_schedule_id' in session:
                        session['active_schedule_id'] = 1
                    return redirect(url_for('stats.overview', schedule_selector=session['active_schedule_id']))
                else:
                    flash("Incorrect password", category='error')
            else:
                flash("User is not verified", category='error')
        else:
            flash("Email does not exist", category='error')

    return render_template_correct_status_code("login.html")


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
            hashed_password = generate_password_hash(password, method="scrypt")
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=hashed_password
            )

            new_user.save_to_db()

            token = jwt.encode(
                {
                    "email_address": new_user.email,
                    "password": new_user.password,
                }, SECRET_KEY
            )
            # login_user(new_user, remember=True)
            flash('User created', category='success')
            # return redirect(url_for('stats.overview', schedule_selector=1))
            gmail.send(
                subject="Workout stats - new user verification",
                receivers=[new_user.email],
                html=VERIFICATION_TEMPLATE,
                body_params={
                    "token": token,
                    "url_for": url_for,
                    "first_name": first_name
                }
            )
            return render_template_correct_status_code("email_sent.html",
                                                       email=email,
                                                       first_name=first_name
                                                       )

    return render_template_correct_status_code("signup.html")


@auth.route("/verify-email/<token>")
def verify_email(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email_address = data["email_address"]
        password = data["password"]
    except Exception:
        return render_template_correct_status_code("signup.html")

    user = User.find_by_email(email_address)
    if user:
        if not user.is_verified:
            if user.password == password:
                user.is_verified = True
                user.save_to_db()
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                if not 'active_schedule_id' in session:
                    session['active_schedule_id'] = 1
                return redirect(url_for('stats.overview', schedule_selector=session['active_schedule_id']))
            else:
                flash("Invalid verification token", category='error')
        else:
            flash("User is already verified", category='error')
    else:
        flash("Email does not exist", category='error')

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
