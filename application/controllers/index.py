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
			username=user_manager.get_user_list(email).username
			session['user_id']=user_manager.get_user_list(email).id
			session['username']=username
			return render_template('layout.html')
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

@app.route('/write',methods=['GET','POST'])
def write():
	if request.method=="POST":
		post=request.form['post']
		user_manager.create(session['user_id'],post,session['wall_id'])
		return redirect(url_for('timeline'))
	else:
		return render_template('write.html')

@app.route('/',defaults={'wall_id':0})
@app.route('/timeline/<int:wall_id>')
def timeline(wall_id):
	user=user_manager.get_user(wall_id)
	username = user.username
	session['wall_id']=wall_id
	session['user_name']=username
	# posts=user_manager.get_post_list(session['wall_id'])
	return render_template('timeline.html',message=username,posts=user.wall_posts)

@app.route('/delete_post/<int:pid>')
def delete_post(pid):
	user_manager.delete_post(pid)
	return redirect(url_for('timeline',wall_id=session['wall_id']))

@app.route('/read/<int:wall_id>/<int:pid>',methods=['GET','POST'])
def read(pid,wall_id):
	if request.method=="POST":
		
		post=user_manager.get_post(pid)
		comments=request.form['comments']
		
		user_manager.comment(session['user_id'],comments,pid)
		return render_template('read.html',post=post,comments=post.comments)
	else:
		user=user_manager.get_user(wall_id)
		post=user_manager.get_post(pid)
		session['pid']=pid
		session['wall_id']=wall_id
		return render_template('read.html',post=post,comments=post.comments)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404