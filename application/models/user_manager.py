#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_
import json

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

def get_post_list(wallid,limit):
	cnt=int(limit)
	post=Post.query.filter(Post.wall_id==wallid).order_by(db.desc(Post.created_time)).slice(cnt,cnt+5).all()
	# post=Post.query.filter_by(wall_id=wallid).all()
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

def modify(post_id,text):
	post=Post.query.get(post_id)
	post.body=text
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

def delete_comment(cid):
	d_comment=Comment.query.get(cid)
	db.session.delete(d_comment)
	db.session.commit()

def add_profile_image(user_id, filename):
	user= get_user(user_id)
	user.profile_image =filename

	db.session.commit()
def add_follow(follower,followee):
	follow=Follow(
		follower_id=follower,
		followee_id=followee
		)
	db.session.add(follow)
	db.session.commit()

def find_user(text):
	user = User.query.filter(User.username.like('%'+text+'%')).all()
	return user

def get_newspeed_post(find_list,cnt):
	posts=Post.query.filter(or_(Post.wall_id.in_(find_list), Post.user_id.in_(find_list) )).order_by(db.desc(Post.created_time)).slice(cnt,cnt+5).all()
	# posts=Post.query.filter(Post.user_id.in_([user_id])).all()
	# filter(or_(User.name == 'ed', User.name == 'wendy'))
	return posts