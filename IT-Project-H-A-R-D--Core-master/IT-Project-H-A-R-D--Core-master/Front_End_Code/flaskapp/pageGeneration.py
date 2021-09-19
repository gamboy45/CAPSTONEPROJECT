from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from base64 import decodestring, encodestring, b64encode

from .queryFuncs import getPerson, getArtifact, getArtifactImages, getPostCard, getLetter, getRelationships, getAssociatedArtifacts, getAssociatedPeople
from .dataModels import FamilyMember, Relationship, Artifact, Letter, PostCard, ArtifactImage, Comment, Entity

import importlib


"""
Renders an artifact page
"""
def displayArtifactPage(artifactID):
	artifact = getArtifact(artifactID)
	images = getArtifactImages(artifactID)

	artifactOwner = getPerson(artifact.CurrentOwner)
	heir = getPerson(artifact.Heir)

	specialisedInfo = None
	specImage = None
	if artifact.Type == 'letter':
		specialisedInfo = getLetter(artifactID)

		if specialisedInfo.Envelope != None:
			specImage = encodestring(specialisedInfo.Envelope).decode("utf-8")

	elif artifact.Type == 'postcard':
		specialisedInfo = getPostCard(artifactID)

		if specialisedInfo.CoverPicture != None:
			specImage = encodestring(specialisedInfo.CoverPicture).decode("utf-8")

	displayableImages = []
	for image in images:
		displayableImages.append((encodestring(image.Image).decode("utf-8"),image.Caption))
		#image.Image = encodestring(image.Image).decode("utf-8")


	associatedPeople = getAssociatedPeople(artifactID)

	return render_template('Artifact_page_template.html', artifact = artifact, images = displayableImages, specInfo = specialisedInfo, specImage = specImage,\
		artifactOwner = artifactOwner, associatedPeople = associatedPeople)


def displayArtifactEditPage(artifactID):
	artifact = getArtifact(artifactID)
	artifactOwner = getPerson(artifact.CurrentOwner)
	heir = getPerson(artifact.Heir)

	return render_template('edit_artifact.html', artifact = artifact, artifactOwner = artifactOwner)



"""
Renders a person's page
"""
def displayPersonPage(personID):

	person = getPerson(personID)
	profilePic = None
	if person.ProfilePic != None:
		image = person.ProfilePic
		profilePic = encodestring(image).decode("utf-8")

	relations = getRelationships(personID)
	relatives = []

	for relationship in relations:

		relative = getPerson(relationship.Individual2)

		relationshipType = relationship.RelationshipType
		relativeName = relative.FirstName + " " + relative.LastName
		relatives.append((relationshipType, relativeName, relative.FamilyMemberID, genPicData(relative.ProfilePic)))
	
	relatives = sortRelative(relatives)
	artifacts = getAssociatedArtifacts(personID)

	return render_template('person_page_template.html',person = person, imageData = profilePic, relatives = relatives, artifacts = artifacts)

def genPicData(dbPic):
	profilePic = None
	if dbPic != None:
		profilePic = encodestring(dbPic).decode("utf-8")
	return profilePic

def sortRelative(list):
	output = []
	parents = 0
	children = 0
	spouse = False
	for i in range(4):
		for relative in list:
			if i == 0 and relative[0] == 'child':
				output.append(relative)
				parents += 1
			elif i == 1 and relative[0] == 'spouse':
				output.append(relative)
				output.append(("self", "self"))
				spouse = True
			elif i == 2  and (relative[0] == 'brother' or relative[0] == 'sister'):
				output.append(relative)
			elif i == 3 and relative[0] == 'parent':
				output.append(relative)
				children += 1
	if not spouse:
		output.insert(parents,("self", "self"))
		output.insert(parents,("nospouse", "nospouse"))
	output.insert(parents, ("linebreak", "linebreak"))
	if parents == 0:
		output.insert(parents, (("noparent", "noparent")))
	if children != 0:
		output.insert(-children, ("linebreak", "linebreak"))
	
	return output

def displayPersonEditPage(personID):
	person = getPerson(personID)
	profilePic = None
	if person.ProfilePic != None:
		image = person.ProfilePic
		profilePic = encodestring(image).decode("utf-8")

	return render_template('edit_person.html',person = person, imageData = profilePic)