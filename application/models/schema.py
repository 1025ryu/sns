from application import db

class User(db.Model):
	id			= db.Column(db.Integer, primary_key=True)
	email		= db.Column(db.String(60))
	username	= db.Column(db.String(45))
	gender		= db.Column(db.Enum('M','F'))
	password	= db.Column(db.String(100))
	mobile		= db.Column(db.String(15))
	birthday	= db.Column(db.Date)

class Post(db.Model):
	id			= db.Column(db.Integer, primary_key=True)
	body		= db.Column(db.Text())
	created_time= db.Column(db.DateTime, default=db.func.now())
	edited_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
	is_edited	= db.Column(db.Boolean, default='0', onupdate='1')
	is_secret	= db.Column(db.Boolean, default='0')
	user_id		= db.Column(db.Integer, db.ForeignKey('user.id'))
	user 		= db.relationship('User',foreign_keys=[user_id])
	wall_id		= db.Column(db.Integer, db.ForeignKey('user.id'))
	wall 		= db.relationship('User',foreign_keys=[wall_id], backref=db.backref('wall_posts', cascade='all,delete-orphan', lazy='dynamic'))

class Comment(db.Model):
	id			= db.Column(db.Integer, primary_key=True)
	body		= db.Column(db.Text())
	created_time= db.Column(db.DateTime, default=db.func.now())
	post_id		= db.Column(db.Integer,  db.ForeignKey('post.id'))
	post 		= db.relationship('Post', backref= db.backref('comments', cascade='all,delete-orphan', lazy='dynamic'))
	user_id		= db.Column(db.Integer, db.ForeignKey('user.id'))
	user 		= db.relationship('User')