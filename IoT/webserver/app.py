from flask import Flask 
from flask import Blueprint, render_template, url_for, request, redirect, flash
from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

auth = Blueprint('auth', __name__)

class User(UserMixin, db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(20))

    def __init__(self, _mail, _pass):
        self.mail = _mail
        self.password = _pass


@auth.route('/', methods=['POST', 'GET'])
def index():
    email = request.form.get('user')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check your login details and try again')
        return redirect('/')


    return redirect(url_for('auth.dashboard'))

@auth.route('/dashboard')
def dashboard():

    return render_template("dashboard.html")        

