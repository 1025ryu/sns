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

def get_user(id):
	return User.query.get(id)

def get_post(pid):
	return Post.query.get(pid)

def login_check(email,password):
	return User.query.filter(User.email==email,User.password==db.func.md5(password)).count()!=0

def get_post_list(wallid):
	post=Post.query.filter_by(wall_id=wallid).all()
	return post

def create(user,text,wall):
	post=Post(
		user_id=user,
		wall_id=wall,
		body=text,
		is_secret='1'
		)
	db.session.add(post)
	db.session.commit()

def comment(user,texts,post):
	comment=Comment(
		user_id=user,
		body=texts,
		post_id=post
		)
	db.session.add(comment)
	db.session.commit()

def delete_post(pid):
	d_post=Post.query.get(pid)
	db.session.delete(d_post)
	db.session.commit()