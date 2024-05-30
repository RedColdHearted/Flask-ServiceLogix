from flask import render_template

def home():
    return render_template('home/home.html')

def login():
    return render_template('registration/login.html')
