from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from db import db
from models import Users
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


@auth.route("/login", methods=["POST", "GET"])
def login():
    e_mail = request.form.get("login_email")
    password = request.form.get("login_password")

    return render_template("login.html")


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("signup_firstName")
        last_name = request.form.get("signup_lastName")
        email = request.form.get("signup_email")
        password = request.form.get("signup_password")

        email_exist = Users.query.filter_by(email=email).first()

        if email_exist:
            flash("This email is already registered.", category='error')
        # Change this later for regex, or check the email_validator package
        elif len(email) < 5:
            flash("Email is invalid.", category='error')
        # Change this later for regex
        elif len(password) < 4:
            flash("Invalid password.", category='error')
        else:
            new_user = Users(
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created')
            return redirect(url_for('stats.overview'))

    return render_template("signup.html")