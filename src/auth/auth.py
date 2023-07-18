from flask import Blueprint, redirect, url_for, render_template, request, session
from datetime import timedelta

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


@auth.route("/login", methods=["POST", "GET"])
def login():
    e_mail = request.form.get("login_email")
    password = request.form.get("login_password")

    return render_template("login.html")


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    first_name = request.form.get("signup_firstName")
    last_name = request.form.get("signup_lastName")
    e_mail = request.form.get("signup_email")
    password = request.form.get("signup_password")

    return render_template("signup.html")