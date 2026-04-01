from flask import Blueprint, render_template, url_for, session, redirect

homesite = Blueprint('homesite', __name__)

@homesite.route('/')
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template('home.html')
