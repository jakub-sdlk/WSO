from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from main import db
from models import User

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

        email_exist = User.query.filter_by(email=email).first()
        if email_exist:
            flash('')

    return render_template("signup.html")