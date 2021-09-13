from langlab import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

	def __repr__(self):
		return f"User('{self.username}, {self.email}')"

class Strain(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(120), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	# one to many references
	links = db.relationship('Link', backref='Strain', lazy=True)
	is_used = db.Column(db.Boolean, nullable=False, default=False)
	used_since = db.Column(db.DateTime, nullable=True)
	active = db.Column(db.Boolean, nullable=False, default=True)

	def __repr__(self):
		linksString=''
		for link in self.links:
			linksString += f"\n{link}"

		return f"""Strain('{self.id}, type: {self.type}, Created: {self.date_created}, is_used: {self.is_used}, used since: {self.used_since}')
			{linksString} <br>
		"""

class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	prev_link_id = db.Column(db.Integer, nullable=False)
	strain_id = db.Column(db.Integer, db.ForeignKey('strain.id'), nullable=False)
	# study_time maybe a good addition ?
	answers = db.relationship('Answer', backref='Link', lazy=True)
	# IF student need to enter a code
	# usercode = db.Column(db.String(120), nullable=True)

	def __repr__(self):
		answerString=''
		for answer in self.answers:
			answerString += f"\n{answer}"

		return f"""<br>Link('{self.id}, {self.prev_link_id}, {self.strain_id}')
			\n{answerString}
		"""

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(120), nullable=False)
	movement_id = db.Column(db.Integer, db.ForeignKey('movement.id'), nullable=False)
	link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)
	movement = db.relationship("Movement", foreign_keys="Answer.movement_id")

	def __repr__(self):
		return f"Answer('{self.id}, {self.content}')"

class Movement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ref_number = db.Column(db.String(120), nullable=False)
	url = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return f"Movement('{self.id}, {self.url}')"
