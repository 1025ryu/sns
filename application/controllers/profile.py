from application import app
from flask import render_template, redirect, url_for, request, session
from application.models.file_manager import *
from application.models.user_manager import *

@app.route('/profile')
def profile():
	user=get_user(session['user_id'])


	return render_template('profile.html',profile_image=user.profile_image)

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

	return redirect(url_for('profile'))

@app.route('/image/profile/<filename>')
def get_profile_image(filename):
	
	directory = '/gs/team-1025ryu/profile/'
	filepath = directory +filename
	return read_file(filepath)