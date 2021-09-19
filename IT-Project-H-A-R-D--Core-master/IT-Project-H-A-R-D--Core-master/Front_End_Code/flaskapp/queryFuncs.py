from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy

from .dataModels import FamilyMember, Relationship, Artifact, Letter, PostCard, ArtifactImage, Comment, Entity, Entity_has_FamilyMember
from . import db
from datetime import datetime


"""
Module for functions involving parsing search input and making dBase queries
"""



"""
Returns a tuple of the parameters provided in the search query.
"""
def parseArtifactSearch(searchQuery):

	##Get all artifact name inputs
	artName = searchQuery['Name']
	if (artName == ""):
		artName = "Null"

	##Get the years for the artifacts
	artYear = searchQuery['Year']
	if (artYear == ""):
		artYear = "Null"

	##Get the tags for the artifacts
	artTag = searchQuery['Tag']
	if (artTag == ""):
		artTag = "Null"

	##Get the name of the associated person
	associatedPerson = searchQuery['Associated Person'].split(' ')

	artType = searchQuery['artifactType']

	if (len(associatedPerson) != 2):
		associatedPerson = ("Null","Person")

	return (artName, artYear, artTag, associatedPerson, artType)


"""
Queries the dBase for the artifacts satisfying the input search parameters
"""
def queryArtifactSearch(searchQuery):
	searchParams = parseArtifactSearch(searchQuery)
	fName = searchParams[3][0]
	lName = searchParams[3][1]

	person = getPersonByName(fName,lName)
	if (person != None):
		associations = Entity_has_FamilyMember.query.join(FamilyMember, FamilyMember.FamilyMemberID == Entity_has_FamilyMember.FamilyMember_FamilyMemberID).filter(Entity_has_FamilyMember.FamilyMember_FamilyMemberID == person.FamilyMemberID).all()

		associatedArtifacts = getAssociatedArtifacts2(person.FamilyMemberID)

		assArtIds = []
		for art in associatedArtifacts:
			assArtIds.append(art.ArtifactID)
	else:
		associatedArtifacts = getAssociatedArtifacts2("Not a valid ID")

	if (searchParams[4] == "all"):
		results = Artifact.query.join(FamilyMember, Artifact.CurrentOwner == FamilyMember.FamilyMemberID).\
			filter((Artifact.Name == searchParams[0]) | (Artifact.DateAcquireYear == searchParams[1]) |\
			(Artifact.Tags == searchParams[2]) | (FamilyMember.FirstName == fName and FamilyMember.LastName == lName))
	else:
		results = Artifact.query.join(FamilyMember, Artifact.CurrentOwner == FamilyMember.FamilyMemberID).\
			filter(((Artifact.Name == searchParams[0]) | (Artifact.DateAcquireYear == searchParams[1]) |\
			(Artifact.Tags == searchParams[2]) | (FamilyMember.FirstName == fName and FamilyMember.LastName == lName)),\
			(Artifact.Type == searchParams[4]))

	return results.union(associatedArtifacts)


"""
Returns the artifact with the input artifactID joined with related entries in other tables
"""
def getArtifact(artifactID):
	result =  Artifact.query.filter(Artifact.ArtifactID == artifactID).first()
	return result

def getArtifactByName(name):
	result = Artifact.query.filter(Artifact.Name == name).first()
	return result

def getArtifactEntity(artifactID):
	return Entity.query.filter(Entity.Artifact_ArtifactID == artifactID).first()

"""
Returns the Artifact Images for a specific artifact
"""
def getArtifactImages(artifactID):
	results = ArtifactImage.query.filter(ArtifactImage.Artifact_ArtifactID == artifactID).all()
	return results

"""
Returns the letter associated with a spcific artifact
"""
def getLetter(artifactID):
	return Letter.query.filter(Letter.Artifact_ArtifactID == artifactID).first()

"""
Returns the postacrd assocaiated with a specfic artifact
"""
def getPostCard(artifactID):
	return PostCard.query.filter(PostCard.Artifact_ArtifactID == artifactID).first()


def addNewArtifact(request):

	artType = request.form['artifactType']

	imageData = (request.files['Image']).read()

	latestArtifact = db.session.query(Artifact).filter(Artifact.ArtifactID == Artifact.ArtifactID).order_by(Artifact.ArtifactID.desc()).first()
	if (latestArtifact == None):
		newID = 0
	else:
		newID = latestArtifact.ArtifactID + 1

	latestImage = db.session.query(ArtifactImage).filter(ArtifactImage.ArtifactImageID == ArtifactImage.ArtifactImageID).order_by(ArtifactImage.ArtifactImageID.desc()).first()
	if (latestImage == None):
		newArtImID = 0
	else:
		newArtImID = latestImage.ArtifactImageID + 1


	currentTime = datetime.now()
	yearAdded = currentTime.year
	monthAdded = currentTime.month
	dayAdded = currentTime.day

	if request.form['YearAcquired'] == "":
		yearAcquired = None
	else:
		yearAcquired = request.form['YearAcquired']
	if request.form['MonthAcquired'] == "":
		monthAcquired = None
	else:
		monthAcquired = request.form['MonthAcquired']
	if request.form['DayAcquired'] == "":
		dayAcquired = None
	else:
		dayAcquired = request.form['DayAcquired']

	ownerName = request.form['CurrentOwner'].split(' ')
	#If no owner entered don't add artifact
	if (len(ownerName) < 2):
		return
	owner = getPersonByName(ownerName[0], ownerName[1])
	#If owner does not exist then don't add artifact
	if (owner == None):
		return

	heirName = request.form['Heir'].split(' ')
	if (len(heirName) > 1):
		heir = getPersonByName(heirName[0], heirName[1])
	else:
		heir = None
	#Create new artifact record
	newArtifact = Artifact(ArtifactID = newID,\
		Name = request.form['Name'],\
		Geotag = request.form['Location'],\
		Tags = request.form['Tag'],\
		Type = artType,\
		description = request.form['Description'],\
		DateAcquireYear = yearAcquired,\
		DateAcquireMonth = monthAcquired,\
		DateAcquireDay = dayAcquired,\
		AccuracyAcquire = request.form['accuracy'],\
		DateAddedYear = yearAdded,\
		DateAddedMonth = monthAdded,\
		DateAddedDay = dayAdded,
		CurrentOwner = owner.FamilyMemberID,\
		Heir = heir)

	db.session.add(newArtifact)
	db.session.commit()

	specImage = (request.files['specImage']).read()
	#Create letter or postcard record
	if artType == 'letter':
		if request.form['letterType'] == "Aerogramme":
			aerogramme = True
			telegram = False
		elif request.form['letterType'] == "Telegram":
			telegram = True
			aerogramme = False
		else:
			aerogramme = False
			telegram = False

		latestLetter = db.session.query(Letter).filter(Letter.LetterID == Letter.LetterID).order_by(Letter.LetterID.desc()).first()
		if (latestLetter == None):
			newSpecID = None
		else:
			newSpecID = latestLetter.LetterID + 1

		newArtSpecifics = Letter(LetterID = newSpecID,\
			SenderAddress = request.form['SenderAddress'],
			ReceiverAddress = request.form['ReceiverAddress'],\
			Sender = request.form['Sender'],\
			Receiver = request.form['Receiver'],
			Aerogramme = aerogramme,\
			Telegram = telegram,\
			Envelope = specImage,\
			Artifact_ArtifactID = newID)
	else:

		latestPostCard = db.session.query(PostCard).filter(PostCard.PostCardID == PostCard.PostCardID).order_by(PostCard.PostCardID.desc()).first()
		if (latestPostCard == None):
			newSpecID = 0
		else:
			newSpecID = latestPostCard.PostCardID + 1

		newArtSpecifics = PostCard(PostCardID = newSpecID,\
			SenderAddress = request.form['SenderAddress'],
			ReceiverAddress = request.form['ReceiverAddress'],\
			Sender = request.form['Sender'],\
			Receiver = request.form['Receiver'],\
			CoverPicture = specImage,\
			Artifact_ArtifactID = newID)

	newArtifactImage = ArtifactImage(Artifact_ArtifactID = newID,\
		ArtifactImageID = newArtImID,\
		Image = imageData,\
		Caption = request.form['imageCaption'])


	#Create new entity object
	latestEntity = db.session.query(Entity).filter(Entity.EntityID == Entity.EntityID).order_by(Entity.EntityID.desc()).first()
	if (latestEntity == None):
		newEntityID = 0
	else:
		newEntityID =latestEntity.EntityID + 1

	newEntity = Entity(EntityID = newEntityID,\
		Name = request.form['Name'],\
		Tag = request.form['Tag'],\
		Artifact_ArtifactID = newID)


	db.session.add(newArtifactImage)
	db.session.add(newArtSpecifics)
	db.session.add(newEntity)
	db.session.commit()

	newEntityPersonAssociation = Entity_has_FamilyMember(Entity_EntityID = newEntityID,\
		FamilyMember_FamilyMemberID = owner.FamilyMemberID)

	db.session.add(newEntityPersonAssociation)
	db.session.commit()


def editArtifact(request, artifactID):
	artifact = getArtifact(artifactID)

	Name = request.form['Name']
	Location = request.form['Location']
	Tags = request.form['Tag']
	YearAcquired = request.form['YearAcquired']
	MonthAcquired = request.form['MonthAcquired']
	DayAcquired = request.form['DayAcquired']
	AccuracyAcquire = request.form['accuracy']
	Description = request.form['Description']

	newOwnerName = request.form['CurrentOwner'].split(' ')
	if (len(newOwnerName) > 1):
		CurrentOwner = getPersonByName(newOwnerName[0], newOwnerName[1])
		if (CurrentOwner != None):
			artifact.CurrentOwner = CurrentOwner.FamilyMemberID
	else:
		CurrentOwner = None

	newHeir = request.form['Heir'].split(' ')
	if (len(newHeir) > 1):
		Heir = getPersonByName(newHeir[0], newHeir[1])
		if (Heir != None):
			artifact.Heir = Heir.FamilyMemberID
	else:
		Heir = None

	if (len(Name) > 0):
		artifact.Name = Name
	if (len(Location) > 0):
		artifact.Location = Location
	if (len(Tags) > 0):
		artifact.Tags = Tags
	if (len(YearAcquired) > 0):
		artifact.YearAcquired = YearAcquired
	if (len(MonthAcquired) > 0):
		artifact.MonthAcquired = MonthAcquired
	if (len(DayAcquired) > 0):
		artifact.DayAcquired = DayAcquired
	if (len(AccuracyAcquire) > 0):
		artifact.AccuracyAcquire = AccuracyAcquire
	if (len(Description) > 0):
		artifact.Des = Description

	db.session.commit()




"""
Creates a new ArtifactImage record for the input artifact and image file
"""
def addNewArtifactImage(request):

	latestImage = db.session.query(ArtifactImage).filter(ArtifactImage.ArtifactImageID == ArtifactImage.ArtifactImageID).order_by(ArtifactImage.ArtifactImageID.desc()).first()
	if (latestImage == None):
		newArtImID = 0
	else:
		newArtImID = latestImage.ArtifactImageID + 1

	artifact = getArtifactByName(request.form['artifact'])
	if (artifact == None):
		return

	imageFile = request.files['image']
	if (imageFile == None):
		return
	imageData = imageFile.read()

	caption = request.form['caption']

	newArtImage = ArtifactImage(ArtifactImageID = newArtImID,\
		Image = imageData,\
		Caption = caption,\
		Artifact_ArtifactID = artifact.ArtifactID)
	db.session.add(newArtImage)
	db.session.commit()
	return


"""
Returns a tuple of the first and list name from the search query.
"""
def parsePersonSearch(searchQuery):
	return (searchQuery['FirstName'], searchQuery['LastName'])


"""
Queries the dBase for the people satisfying the input search parameters
"""
def queryPeopleSearch(searchQuery):
	searchParams = parsePersonSearch(searchQuery)
	if (searchParams[0] == ""):
		results = results = FamilyMember.query.filter((FamilyMember.LastName == searchParams[1]))
	elif (searchParams[1] == ""):
		results = FamilyMember.query.filter((FamilyMember.FirstName == searchParams[0]))
	else:
		results = FamilyMember.query.filter((FamilyMember.FirstName == searchParams[0]) | (FamilyMember.LastName == searchParams[1]))
	return results

"""
Returns the person referred to by the personID
"""
def getPerson(personID):
	result = db.session.query(FamilyMember).filter(FamilyMember.FamilyMemberID == personID).first()
	return result

"""
Returns the relationships in which the person defined by personID is the individual1
"""
def getRelationships(personID):
	return Relationship.query.filter(Relationship.Individual1 == personID).all()


"""
Returns the artifacts associated with a particular person
"""
def getAssociatedArtifacts(personID):
	entityRelations = Entity_has_FamilyMember.query.filter(Entity_has_FamilyMember.FamilyMember_FamilyMemberID == personID).all()
	associatedArtifactIDs = []

	for relation in entityRelations:
		associatedArtifactIDs.append(Entity.query.filter(Entity.EntityID == relation.Entity_EntityID).first().Artifact_ArtifactID)

	associatedArtifacts = []

	for ID in associatedArtifactIDs:
		associatedArtifacts.append(Artifact.query.filter(Artifact.ArtifactID == ID).first())
	return associatedArtifacts

"""
Returns the artifacts associated with a particular person
"""
def getAssociatedArtifacts2(personID):
	entityRelations = Entity_has_FamilyMember.query.filter(Entity_has_FamilyMember.FamilyMember_FamilyMemberID == personID).all()
	associatedArtifactIDs = []

	for relation in entityRelations:
		associatedArtifactIDs.append(Entity.query.filter(Entity.EntityID == relation.Entity_EntityID).first().Artifact_ArtifactID)

	associatedArtifacts = Artifact.query.filter(Artifact.ArtifactID == "Not a valid ID")

	for ID in associatedArtifactIDs:
		associatedArtifacts = associatedArtifacts.union(Artifact.query.filter(Artifact.ArtifactID == ID))
	return associatedArtifacts



"""
Returns the people associated with a particular artifact
"""
def getAssociatedPeople(artifactID):
	#entity = Entity.query.filter(Entity.Artifact_ArtifactID == artifactID).first()

	personIDs = []


	relations = Entity_has_FamilyMember.query.filter(Entity_has_FamilyMember.Entity_EntityID == artifactID).all()
	for relation in relations:
		personIDs.append(relation.FamilyMember_FamilyMemberID)
	
	associatedPeople = []

	for ID in personIDs:
		associatedPeople.append(getPerson(ID))
	return associatedPeople




"""
Returns the first person to have the first and last names provided, or None if there are no matches
"""
def getPersonByName(firstName, lastName):
	return db.session.query(FamilyMember).filter(FamilyMember.FirstName == firstName, FamilyMember.LastName == lastName).first()


def addNewPerson(request):
	latestPerson = db.session.query(FamilyMember).filter(FamilyMember.FamilyMemberID == FamilyMember.FamilyMemberID).order_by(FamilyMember.FamilyMemberID.desc()).first()
	if (latestPerson == None):
		newID = 0
	else:
		newID = latestPerson.FamilyMemberID + 1

	imageFile = request.files['Image']
	imageData = imageFile.read()

	if (request.form['DODYear'] == ""):
		DODYear = None
	else:
		DODYear = request.form['DODYear']
	if (request.form['DODMonth'] == ""):
		DODMonth = None
	else:
		DODMonth = request.form['DODMonth']
	if (request.form['DODDay'] == ""):
		DODDay = None
	else:
		DODDay = request.form['DODDay']
	if (request.form['DOBYear'] == ""):
		DOBYear = None
	else:
		DOBYear = request.form['DOBYear']
	if (request.form['DOBMonth'] == ""):
		DOBMonth = None
	else:
		DOBMonth = request.form['DOBMonth']
	if (request.form['DOBDay'] == ""):
		DOBDay = None
	else:
		DOBDay = request.form['DOBDay']
	
	
	newPerson = FamilyMember(FamilyMemberID = newID,\
	            FirstName = request.form['FirstName'],\
	            LastName = request.form['LastName'],\
	            ProfilePic = imageData,\
	            Gender = request.form['gender'],\
	            MaidenName = request.form['MaidenName'],\
	            DODYear = DODYear,\
	            DODMonth = DODMonth,\
	            DODDay = DODDay,\
	            DOBYear = DOBYear,\
	            DOBMonth = DOBMonth,\
	            DOBDay = DOBDay,\
	            AccuracyDOD = request.form['DODaccuracy'],\
	            AccuracyDOB = request.form['DOBaccuracy'])
	db.session.add(newPerson)
	db.session.commit()
	return

"""
Edits an existing person's data
"""
def editPerson(request, personID):
	reqForm = request.form
	person = getPerson(personID)

	ProfilePic = request.files['Image']
	imageData = ProfilePic.read()

	FirstName = reqForm['FirstName']
	LastName = reqForm['LastName']
	MaidenName = reqForm['MaidenName']
	Gender = reqForm['gender']
	DODYear = request.form['DODYear']
	DODMonth = reqForm['DODMonth']
	DODDay = reqForm['DODDay']
	DOBYear = reqForm['DOBYear']
	DOBMonth = reqForm['DOBMonth']
	DOBDay = reqForm['DOBDay']
	AccuracyDOB = reqForm['DOBaccuracy']
	AccuracyDOD = reqForm['DODaccuracy']

	if (len(FirstName) > 0):
		person.FirstName = FirstName

	if (len(LastName) > 0):
		person.LastName =LastName

	if (len(MaidenName) > 0):
		person.MaidenName = MaidenName

	if (len(Gender) > 0):
		person.Gender = Gender

	if (len(DODYear) > 0):
		person.DODYear = DODYear

	if (len(DODMonth) > 0):
		person.DODMonth = DODMonth

	if (len(DODDay) > 0):
		person.DODDay = DODDay

	if (len(DOBYear) > 0):
		person.DOBYear = DOBYear

	if (len(DOBMonth) > 0):
		person.DOBMonth = DOBMonth

	if (len(DOBDay) > 0):
		person.DOBDay = DOBDay

	if (len(AccuracyDOD) > 0):
		person.AccuracyDOD = AccuracyDOD

	if (len(AccuracyDOB) > 0):
		person.AccuracyDOB = AccuracyDOB

	if (len(imageData) > 0):
		person.ProfilePic = imageData

	db.session.commit()


def addNewFamilyRelationship(request):

	latestRelationship = db.session.query(Relationship).filter(Relationship.RelationshipID == Relationship.RelationshipID).order_by(Relationship.RelationshipID.desc()).first()
	if (latestRelationship == None):
		newID = 0
	else:
		newID = latestRelationship.RelationshipID + 1

	person1Name = request.form['person1'].split(' ')
	person2Name = request.form['person2'].split(' ')

	if ((len(person1Name) < 2) or (len(person2Name) < 2)):
		return
	else:
		person1 = getPersonByName(person1Name[0], person1Name[1])
		person2 = getPersonByName(person2Name[0], person2Name[1])

		newRelationship = Relationship(RelationshipID = newID,\
			Individual1 = person1.FamilyMemberID,\
			Individual2 = person2.FamilyMemberID,\
			RelationshipType = request.form['Relationship'])
		db.session.add(newRelationship)
		db.session.commit()
	return



def addNewArtifactRelationship(request):
	personName = request.form['person'].split(' ')
	#If no owner entered don't add association
	if (len(personName) < 2):
		return
	person = getPersonByName(personName[0], personName[1])
	#If owner does not exist then don't add association
	if (person == None):
		return

	artifact = getArtifactByName(request.form['artifact'])

	if (artifact == None):
		return

	entity = getArtifactEntity(artifact.ArtifactID)
	if (entity == None):


		newEntity = Entity(EntityID = artifact.ArtifactID,\
		Artifact_ArtifactID = artifact.ArtifactID)
		db.session.add(newEntity)
		db.session.commit()



	newRelationship = Entity_has_FamilyMember(Entity_EntityID = artifact.ArtifactID,\
		FamilyMember_FamilyMemberID = person.FamilyMemberID)

	db.session.add(newRelationship)
	db.session.commit()

	return
