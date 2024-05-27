from flask import request, render_template, jsonify

def register_routes(app, db):
    @app.route('/')
    def home():
        return render_template('home/home.html')
