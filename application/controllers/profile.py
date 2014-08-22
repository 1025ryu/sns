from application import app
from flask import render_template, redirect, url_for, request, session
from application.models.file_manager import *
from application.models.user_manager import *
from flask.ext.wtf import Form
from wtforms import(
	StringField,
	PasswordField,
	SelectField
	)
from wtforms import validators

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

@app.route('/edit_profile/<int:user_id>',methods=['GET','POST'])
def edit_profile(user_id):

	if request.method=="POST":
		form=Editform()
		if form.validate_on_submit():
			edit_user(session['user_id'],form.data)
			image_file = request.files['profile_image']
			filename = image_file.filename
			extension = filename.split('.')[-1]
			new_file_name = str(session['user_id'])+'.'+extension

			directory = '/gs/team-1025ryu/profile/'

			filepath = directory + new_file_name

			save_file(image_file,filepath)
			add_profile_image(session['user_id'],new_file_name)
			return render_template('layout.html')
		else:
			return render_template('edit_profile.html',form=form,user_id=user_id)
	else:
		user=get_user(user_id)
		form=Editform(
			mobile=user.mobile,
			gender=user.gender,
			username=user.username,
			birthday=user.birthday
			)

		return render_template('edit_profile.html',profile_image=user.profile_image,user_id=user_id,form=form,user=user)

@app.route('/profile')
def profile():
	user=get_user(session['user_id'])


	return render_template('edit_profile.html',profile_image=user.profile_image)

@app.route('/upload_image',methods=['POST'])
def upload_image():

	image_file = request.files['profile_image']
	filename = image_file.filename
	extension = filename.split('.')[-1]
	new_file_name = str(session['user_id'])+'.'+extension

	directory = '/gs/team-1025ryu/profile/'

	filepath = directory + new_file_name

	save_file(image_file,filepath)
	add_profile_image(session['user_id'],new_file_name)

	return redirect(url_for('edit_profile'))

@app.route('/image/profile/<filename>')
def get_profile_image(filename):
	
	directory = '/gs/team-1025ryu/profile/'
	filepath = directory +filename
	return read_file(filepath)