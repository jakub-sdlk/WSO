from flask import Blueprint, redirect, url_for, render_template, request, session
from datetime import timedelta

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

@auth.route("/login", methods=["POST", "GET"])
def login():
        return render_template("login.html")

@auth.route("/signup", methods=["POST", "GET"])
def signup():
        return render_template("signup.html")