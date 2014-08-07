#-*- coding:utf-8 -*-
from application import app
from flask import render_template, redirect, url_for,session, request
from application.models.schema import *
from application.models import user_manager

@app.route('/')
def index():
	return render_template('layout.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="POST":
		email=request.form['email']
		password=request.form['password']
		if user_manager.login_check(email,password):
			session['email']=request.form['email']
			return render_template('timeline.html')
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')
		
@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=="POST":
		user_manager.add_user(request.form)
		return render_template('signup.html')
	else:
		return render_template('signup.html')

@app.route('/write')
def write():
	return render_template('write.html')

@app.route('/timeline')
def timeline():
	return render_template('timeline.html')

@app.route('/read')
def read():
	return render_template('read.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404