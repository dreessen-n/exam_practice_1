# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt


# Create the routes
@app.route('/starter')
def show_template():
    """Show starter template"""
    return render_template('starter_1col.html')

