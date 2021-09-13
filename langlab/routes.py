from flask import Flask, render_template, url_for, flash, redirect, session, request
from sqlalchemy import func
from langlab import app, db, bcrypt
from langlab.models import User, Strain, Link, Answer, Movement
from forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

# TODO:
@app.route("/study")
def study():
	studyTime = 30
	currentTime = datetime.utcnow()

	# check existence of studyStart session value
	if session.get('studyStart') and session.get('lastLink'):
		# create datetime obj from session str variable
		studyStart = datetime.strptime(session['studyStart'], '%d/%m/%y %H:%M:%S')
		# get time variation since study start
		timeSinceStart = currentTime - studyStart
		# get the last link
		lastLink = getLinkById(session['lastLink'])

		print("STUDY WITH SESSION VARIABLES")
		print(session['studyStart'])
		print(session['lastLink'])

		# if time is up redirect to answer
		if timeSinceStart > timedelta(minutes=studyTime) or session.get('answeringStart'):
			return render_template('Answer.html', title='Answer', lastLink=lastLink)
		# if time is not up, grab the last link of my strain
		else:
			return render_template('study.html', title='Study', lastLink=lastLink)

	# create session variable and return strain
	else:
		lastLink, usedSince = grabstrain()
		session['lastLink'] = lastLink.id
		session['studyStart'] = usedSince.strftime('%d/%m/%y %H:%M:%S')

	print("FRESH STUDY")

	return render_template('study.html', title='Study', lastLink=lastLink)

# TODO:
@app.route("/answer", methods=['GET', 'POST'])
def answer():

	# add a link and free the link, if you are sending data over
	if request.method == 'POST':
		lastLink = getLinkById(session['lastLink'])
		createNewLink( lastLink.strain_id, lastLink.id, request.form)
		freeStrain(lastLink.strain_id)
		session.pop('lastLink')
		session.pop('studyStart')
		session.pop('answeringStart')

		return redirect(url_for('home'))

	# TODO: Modify the prebuilt answer Time
	answerTime = 30

	if session.get('studyStart') and session.get('lastLink'):

		# get the last link
		lastLink = getLinkById(session['lastLink'])

		# Should only trigger once, the first time you  start answering
		if not session.get('answeringStart'):
			session['answeringStart'] = datetime.utcnow().strftime('%d/%m/%y %H:%M:%S')

		return render_template('answer.html', title="Answer", lastLink=lastLink)

	else:
		return render_template('/')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return redirect(url_for('controlboard'))
	return render_remplate('login.html', title='login', form=form)

@app.route("/controlboard")
def controlboard():
	return render_remplate('controlboard')

### TESTING ROUTES ###
@app.route("/datagen")
def datagen():

	# reset DB
	db.drop_all()

	#create a user
	db.create_all()
	hashed_pword = bcrypt.generate_password_hash('testpassword').decode('utf-8')
	user_1 = User(username='aaronadmin', email='test@test.com', password=hashed_pword)
	db.session.add(user_1)

	#create Movements
	movement_1 = Movement(ref_number='movement1', url='https://www.youtube.com/embed/rsOXquEddSw')
	movement_2 = Movement(ref_number='movement2', url='https://www.youtube.com/embed/LGhaCkhqne8')
	movement_3 = Movement(ref_number='movement3', url='https://www.youtube.com/embed/oT7Q3j2ugvk')

	db.session.add(movement_1)
	db.session.add(movement_2)
	db.session.add(movement_3)

	# create a strain
	type = 'test'
	date_created = datetime.utcnow()
	active = True
	test_strain = Strain(type=type, date_created=date_created, active=active)

	db.session.add(test_strain)
	db.session.commit()

	#grab strain
	my_strain = Strain.query.first()

	#create a link
	prev_link_id = -1
	strain_id = my_strain.id
	link = Link(prev_link_id = prev_link_id, strain_id=strain_id)
	db.session.add(link)

	#grab link
	my_link = Link.query.first()

	#create answers
	answer_1 = Answer(content='answer1', movement_id=1, link_id=my_link.id)
	answer_2 = Answer(content='answer2', movement_id=2, link_id=my_link.id)
	answer_3 = Answer(content='answer3', movement_id=3, link_id=my_link.id)

	db.session.add(answer_1)
	db.session.add(answer_2)
	db.session.add(answer_3)

	db.session.commit()
	return render_template('home.html')

@app.route("/strain/<int:strain_id>")
def showdata(strain_id):
	strain = Strain.query.filter_by(id = strain_id).first()
	return f"{strain}"

# Used to flag a strain as usable and return the last_link of this
# return: last link used, time since the strain is used
def grabstrain():
	# grab a unused strain
	a_strain = Strain.query.filter_by(is_used = False).first()

	# mark Strain as in use and mark
	a_strain.is_used = True
	a_strain.used_since = datetime.utcnow()
	db.session.commit()

	# grab all links of strain and grab last link
	strain_links = a_strain.links
	last_link = strain_links[-1]

	return last_link, a_strain.used_since

def getLinkById(strainid):
	link = Link.query.filter_by(id=strainid).first()
	return link

# add a link to a pre-existing strain
# P.S answers should be a list of tuples with (movement_id, content) format
def createNewLink(my_strain, prev_link_id, answers):
	link = Link(prev_link_id = prev_link_id, strain_id=my_strain)
	db.session.add(link)
	db.session.commit()

	my_link = Link.query.filter_by(prev_link_id = prev_link_id).first()

	# for all answers provided
	print(answers)
	for answer in answers:
		# TODO: TEST THIS SHIT
		print(answer)
		print(answers[answer])
		new_answer = Answer(content=answers[answer], movement_id=answer, link_id=my_link.id)
		db.session.add(new_answer)

	# add all the answer to the DB
	db.session.commit()

	return 1

# Used to flag a strain as usable
def freeStrain(id):
	strain = Strain.query.filter_by(id=id).first()
	strain.is_used = False
	db.session.commit()

	return 1

@app.route("/resetsession")
def refreshSession():

	sessionVarNames = []

	for sessionVar in session:
		sessionVarNames.append(sessionVar)

	for varName in sessionVarNames:
		session.pop(varName)

	#session.pop('lastLink')
	#session.pop('studyStart')
	#session.pop('answeringStart')

	return redirect(url_for("home"))
