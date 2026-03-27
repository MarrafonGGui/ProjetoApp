from flask import Blueprint, render_template, url_for

homesite = Blueprint('homesite', __name__)

@homesite.route('/')
def home():
    return render_template('home.html')

