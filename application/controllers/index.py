#-*- coding:utf-8 -*-
from application import app
from flask import render_template, redirect, url_for,session, request
from application.models.schema import *
from application.models import user_manager
import json
from flask.ext.wtf import Form
from wtforms import(
	StringField,
	PasswordField,
	SelectField
	)
from wtforms import validators
class Userform(Form):
	email=StringField(
		u'email',
		[
			validators.data_required(message=u'please enter your email'),
			validators.Email(message=u'use email form')
		],
		description={'placeholder':u'a@mail.com'}
	)

	password=PasswordField(
		u'password',
		[
			validators.data_required(message=u'please enter your password'),
		],
		description={'placeholder':u'enteryour password'}
	)

class Editform(Form):
	password=PasswordField(
		u'password',
		[
			validators.data_required(message=u'please enter your password'),
			validators.Length(min=8, max=20, message=u'please enter 8~20 password')
		],
		description={'placeholder':u'enteryour password'}
	)

	password_check=PasswordField(
		u'password_check',
		[
			validators.data_required(message=u'please enter your password_check'),
			validators.EqualTo('password', message=u'not same')		
		],
		description={'placeholder':u'enteryour password_check'}
	)
	mobile=StringField(
		u'mobile',
		[
			validators.data_required(message=u'please enter your mobile'),
		],
		description={'placeholder':u'010-1111-1234'}
	)
	gender=SelectField(u'Gender', choices=[('M','male'),('F','female')],coerce=unicode)

	username=StringField(
		u'username',
		[
			validators.data_required(message=u'please enter your name'),
		],
		description={'placeholder':u'huhu'}
	)
	birthday=StringField(
		u'birthday',
		[
			validators.data_required(message=u'please enter your birthday'),
		],
		description={'placeholder':u'1992.01.11'}
	)

class Signform(Form):
	email=StringField(
		u'email',
		[
			validators.data_required(message=u'please enter your email'),
			validators.Email(message=u'use email form')
		],
		description={'placeholder':u'a@mail.com'}
	)

	password=PasswordField(
		u'password',
		[
			validators.data_required(message=u'please enter your password'),
			validators.Length(min=8, max=20, message=u'please enter 8~20 password')
		],
		description={'placeholder':u'enteryour password'}
	)

	password_check=PasswordField(
		u'password_check',
		[
			validators.data_required(message=u'please enter your password_check'),
			validators.EqualTo('password', message=u'not same')		
		],
		description={'placeholder':u'enteryour password_check'}
	)
	mobile=StringField(
		u'mobile',
		[
			validators.data_required(message=u'please enter your mobile'),
		],
		description={'placeholder':u'010-1111-1234'}
	)
	gender=SelectField(u'Gender', choices=[('M','male'),('F','female')],coerce=unicode)

	username=StringField(
		u'username',
		[
			validators.data_required(message=u'please enter your name'),
		],
		description={'placeholder':u'huhu'}
	)
	birthday=StringField(
		u'birthday',
		[
			validators.data_required(message=u'please enter your birthday'),
		],
		description={'placeholder':u'1992.01.11'}
	)


@app.route('/')
def index():
	return render_template('layout.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="POST":
		form=Userform()
		if form.validate_on_submit():
			
			if user_manager.login_check(form.email.data, form.password.data):
				user=user_manager.get_user_list(form.email.data)
				session['email']=form.email.data
				session['username']=user.username
				session['user_id']=user.id
				session['logged_in'] = True
				
				return render_template('layout.html')
			else:
				login_error="wrong email or password"
				return render_template('login.html',form=form,login_error=login_error)
		# email=request.form['email']
		# password=request.form['password']
		# if user_manager.login_check(email,password):
		# 	session['email']=request.form['email']
		# 	username=user_manager.get_user_list(email).username
		# 	session['user_id']=user_manager.get_user_list(email).id
		# 	session['username']=username
		# 	session['logged_in'] = True
		# 	return render_template('layout.html')
		else:
			login_error="wrong email or password"
			return render_template('login.html',form=form,login_error=login_error)
	else:
		form=Userform()
		return render_template('login.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=="POST":
		form=Signform()
		if form.validate_on_submit():
			user_manager.add_user(form.data)
			return render_template('layout.html',form=form)

		else:
			return render_template('signup.html',form=form)
	else:
		form=Signform()
		return render_template('signup.html',form=form)

@app.route('/write',methods=['GET','POST'])
def write():
	if request.method=="POST":
		post=request.form['post']
		user_manager.create(session['user_id'],post,session['wall_id'])
		return redirect(url_for('timeline',wall_id=session['wall_id']))
	else:
		return render_template('write.html')

@app.route('/',defaults={'wall_id':0})
@app.route('/timeline/<int:wall_id>')
def timeline(wall_id):
	user=user_manager.get_user(wall_id)
	user_name = user.username
	session['wall_id']=wall_id
	session['user_name']=user_name
	# data={}
	# db_list=[]
	# posts=user_manager.get_post_list(session['wall_id'])
	# for post in posts:
	# 	data['created_time']=str(post.created_time)
	# 	data['id']=post.id
	# 	data['body']=post.body
	# 	data['edited_time']=str(post.edited_time)
	# 	data['is_edited']=post.is_edited
	# 	data['is_secret']=post.is_secret
	# 	data['user_id']=post.user_id	
	# 	data['wall_id']=post.wall_id
	# 	db_list.append(data)
	# result_list = json.dumps(db_list)
	return render_template('timeline.html',message=user_name)
	# return render_template('timeline.html',message=user_name,list=json.dumps(db_list))
	# return render_template('log.html',log=db_list)

@app.route('/delete_post/<int:pid>')
def delete_post(pid):
	user_manager.delete_post(pid)
	return redirect(url_for('timeline',wall_id=session['wall_id']))

@app.route('/delete_comment/<int:pid>/<int:cid>')
def delete_comment(pid,cid):
	user_manager.delete_comment(cid)
	return redirect(url_for('read',pid=session['pid'],wall_id=session['wall_id']))

@app.route('/modify/<int:pid>',methods=['GET','POST'])
def modify(pid):
	if request.method=="POST":
		text=request.form['post']
		user_manager.modify(pid,text)
		return redirect(url_for('read',pid=session['pid'],wall_id=session['wall_id']))
	else:
		post=user_manager.get_post(pid)
		return render_template('edit.html',post=post)

# @app.route('/edit_profile/<int:user_id>',methods=['GET','POST'])
# def edit_profile(user_id):
# 	if request.method=="POST":
# 		form=Editform()
# 		if form.validate_on_submit():
# 			user_manager.edit_user(session['user_id'],form.data)
# 			return render_template('layout.html')
# 		else:
# 			return render_template('edit_profile.html',form=form,user_id=user_id)
# 	else:
# 		user=user_manager.get_user(user_id)
# 		form=Editform(
# 			mobile=user.mobile,
# 			gender=user.gender,
# 			username=user.username,
# 			birthday=user.birthday
# 			)

# 		return render_template('edit_profile.html',profile_image=user.profile_image,user_id=user_id,form=form,user=user)

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
@app.route('/logout')
def logout():
	session.clear()
	return render_template('layout.html')

@app.route('/find',methods=['GET','POST'])
def find():
	if request.method=='POST':
		text=request.form['text']
		users=user_manager.find_user(text)
		return render_template('user_list.html',users=users)
	else:
		return render_template('find.html')

@app.route('/add_follow/<int:user_id>')
def add_follow(user_id):
	follower_id=session['user_id']
	followee_id=user_id
	if followee_id!=follower_id:
		user_manager.add_follow(follower_id,followee_id)
	return redirect(url_for('find'))

@app.route('/follow')
def follow():
	user=user_manager.get_user(session['user_id'])
	return render_template('follow.html',followers=user.followers,followees=user.followees)

@app.route('/show', methods=['GET','POST'])
def show():
	if request.method == 'POST':
		# raise ValueError(request.form['id'])
		cnt=request.form['cnt']
		cnt=int(cnt)
		posts=user_manager.get_post_list(session['wall_id'],cnt)
		return render_template('show.html',posts=posts)
	else:
		return render_template('show.html',posts=posts)

@app.route('/newspeed', methods=['GET','POST'])
def newspeed():
	if request.method == 'POST':
		cnt=request.form['cnt']
		cnt=int(cnt)
		user_id=session['user_id']
		user=user_manager.get_user(session['user_id'])
		followees=user.followees
		followee_list=[]
		followee_list.append(user_id)
		for followee in followees:
			followee_id=followee.followee.id
			followee_list.append(followee_id)
		posts=user_manager.get_newspeed_post(followee_list,cnt)
		return render_template('newspeed_show.html',posts=posts)
	else:
		user_id=session['user_id']
		user=user_manager.get_user(session['user_id'])
		followees=user.followees
		followee_list=[]
		followee_list.append(user_id)
		for followee in followees:
			followee_id=followee.followee.id
			followee_list.append(followee_id)
		posts=user_manager.get_newspeed_post(followee_list,0)
		return render_template('newspeed.html',posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404