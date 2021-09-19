#!/usr/bin/env python
#
#--------------------------------------------------------------------------

import sys

from datetime import datetime

#--------------------------------------------------------------------------

from flask import render_template, flash, redirect, session, url_for, request

#--------------------------------------------------------------------------

from . import app, db

from .trace   import Trace
from .queryFuncs import queryPeopleSearch, queryArtifactSearch, addNewPerson, addNewArtifact,\
 addNewFamilyRelationship, addNewArtifactRelationship, addNewArtifactImage, editPerson, editArtifact
from .pageGeneration import displayArtifactPage, displayPersonPage, displayPersonEditPage, displayArtifactEditPage

#--------------------------------------------------------------------------

"""
Go to login if not logged in, otherwise go to main page
"""
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('main_page_template.html')

#--------------------------------------------------------------------------

"""
Deal with login, currently uses hardcoded username/password
Could change to a list fo usernames/passwords or use a dBase query to get them.
"""
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
	if (request.method == 'GET'):
		return home()
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True
		return home()
	else:
		flash('wrong password')
		return home()

#--------------------------------------------------------------------------

"""
Handles inputs to searches for artifacts
"""
@app.route('/search/artifacts', methods=['GET', 'POST'])
def search_artifacts():
	if not session.get('logged_in'):
		return home()
	else:
		return render_template('artifacts_search_page.html')

#--------------------------------------------------------------------------

"""
Handles inputs to searches for people
"""
@app.route('/search/people', methods=['GET', 'POST'])
def search_people():
	if not session.get('logged_in'):
		return home()
	else:
		return render_template('people_search_page.html')

#--------------------------------------------------------------------------

"""
Displays the results from a search for people
Actual searching still needs implementation
"""
@app.route('/search/people_results', methods=['GET', 'POST'])
def search_people_results():
	if not session.get('logged_in'):
		return home()
	else:
		if (request.method == 'GET'):
			return search_people()
		else:
			search_query = request.form

			##query the database based on the search query
			results = queryPeopleSearch(search_query)
			return render_template('people_search_results.html', request = search_query, results = results)

#--------------------------------------------------------------------------

"""
Displays the results from a search for artifacts
Actual searching still needs implementation
"""
@app.route('/search/artifact_results', methods=['GET', 'POST'])
def search_artifacts_results():
	if not session.get('logged_in'):
		return home()
	else:
		if (request.method == 'GET'):
			return search_artifacts()
		else:
			results = queryArtifactSearch(request.form)
			return render_template('artifact_search_results.html', names = request.form['Name'], results = results)

#--------------------------------------------------------------------------

"""
Render the person page specified by the id from the post
Getting person's info from dBase still needs to be implemented.
"""
@app.route('/person_page/<personID>', methods=['GET', 'POST'])
def person_page(personID):
	if not session.get('logged_in'):
		return home()
	else:
		userID = personID
		return displayPersonPage(personID)


@app.route('/editPersonData/<personID>', methods = ['GET', 'POST'])
def edit_person_page(personID):
	if (request.method == 'GET'):
		return displayPersonEditPage(personID)
	else:
		editPerson(request, personID)
		return displayPersonPage(personID)


#--------------------------------------------------------------------------

"""
Render the artifact page specified by the id from the post
Getting artifact's info from dBase still needs to be implemented.
"""
@app.route('/artifact_page/<artifactID>', methods=['GET', 'POST'])
def artifact_page(artifactID):
	if not session.get('logged_in'):
		return home()
	else:
		artifactID = artifactID
		return displayArtifactPage(artifactID)


@app.route('/editArtifactData/<artifactID>', methods = ['GET', 'POST'])
def eddit_artifact_page(artifactID):
	if (request.method == 'GET'):
		return displayArtifactEditPage(artifactID)
	else:
		editArtifact(request, artifactID)
		return displayArtifactPage(artifactID)

#--------------------------------------------------------------------------

"""
Logs out of the session
"""
@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()

#--------------------------------------------------------------------------

@app.route('/addPersonData', methods = ['GET', 'POST'])
def addPersonData():
	if (request.method == 'GET'):
		return render_template('add_person.html')
	else:
		addNewPerson(request)
		return render_template('add_person.html')


#--------------------------------------------------------------------------

@app.route('/addFamilyRelationship', methods = ['GET', 'POST'])
def addFamilyRelationship():
	if (request.method == 'GET'):
		return render_template('add_person.html')
	else:
		addNewFamilyRelationship(request)
		return render_template('add_person.html')

#--------------------------------------------------------------------------

@app.route('/addArtifactRelationship', methods = ['GET', 'POST'])
def addArtifactRelationship():
	if (request.method == 'GET'):
		return render_template('add_person.html')
	else:
		addNewArtifactRelationship(request)
		return render_template('add_person.html')

#--------------------------------------------------------------------------

@app.route('/addArtifactData', methods = ['GET', 'POST'])
def addArtifactData():
	if (request.method == 'GET'):
		return render_template('add_artifact.html')
	else:
		addNewArtifact(request)
		return render_template('add_artifact.html')

#--------------------------------------------------------------------------

@app.route('/addNewImage', methods = ['GET', 'POST'])
def addImage():
	if (request.method == 'GET'):
		return render_template('add_artifact.html')
	else:
		addNewArtifactImage(request)
		return render_template('add_artifact.html')
#--------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()

#--------------------------------------------------------------------------