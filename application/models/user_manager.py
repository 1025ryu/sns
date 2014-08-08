from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *

def add_user(data):
	user = User(
		email 	 = data['email'],
		username = data['username'],
		gender	 = data['gender'],
		password = db.func.md5(data['password']),
		mobile	 = data['phone'],
		birthday = data['birthday']
	)
	db.session.add(user)
	db.session.commit()

def get_user_list(mail):
	user=User.query.filter_by(email=mail).first()
	return user
def get_username(id):
	return User.query.get(id)
def login_check(email,password):
	return User.query.filter(User.email==email,User.password==db.func.md5(password)).count()!=0

def create(text):
	post=Post(
		user_id=session['username'],
		wall_id=session['wall_id'],
		body=text,
		is_secret='1'
		)
	db.session.add(post)
	db.session.commit()