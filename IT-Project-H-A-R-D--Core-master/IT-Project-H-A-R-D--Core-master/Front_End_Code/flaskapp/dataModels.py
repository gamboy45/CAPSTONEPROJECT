from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import db
import enum

"""
Note that Images are being referred to by their URL.
They could also be refered to as a LargeBinary, but it would require
that they be converted to base64 in order to be represented in html.
"""


class FamilyMember(db.Model):
	__tablename__ = 'FamilyMember'

	FamilyMemberID = db.Column(db.Integer, primary_key = True)
	FirstName = db.Column(db.String(45))
	LastName = db.Column(db.String(45))
	MaidenName = db.Column(db.String(45))
	DODYear = db.Column(db.Integer)
	DODMonth = db.Column(db.Integer)
	DODDay = db.Column(db.Integer)
	DOBYear = db.Column(db.Integer)
	DOBMonth = db.Column(db.Integer)
	DOBDay = db.Column(db.Integer)
	Gender = db.Column(db.Enum('m', 'f'))
	ProfilePic = db.Column(db.BLOB)
	AccuracyDOD = db.Column(db.Enum('documented', 'accurate', 'likely'))
	AccuracyDOB = db.Column(db.Enum('documented', 'accurate', 'likely'))


##Relationship table
class Relationship(db.Model):
	__tablename__ = 'Relationship'

	RelationshipID = db.Column(db.Integer, primary_key = True)
	Individual1 = db.Column(db.Integer, db.ForeignKey('FamilyMember.FamilyMemberID'), nullable = False)
	Individual2 = db.Column(db.Integer, db.ForeignKey('FamilyMember.FamilyMemberID'), nullable = False)
	RelationshipType = db.Column(db.Enum('child', 'parent', 'spouse', 'grandchild', 'brother', 'sister', 'uncle', 'aunt'), nullable = False)


"""
Table for the artifacts
"""
class Artifact(db.Model):
	__tablename__ = 'Artifact'

	ArtifactID = db.Column(db.Integer, primary_key = True)
	Name = db.Column(db.String(30))
	Geotag = db.Column(db.String(45))
	Tags = db.Column(db.Text)
	DateAddedYear = db.Column(db.Integer)
	DateAddedMonth = db.Column(db.Integer)
	DateAddedDay = db.Column(db.Integer)
	DateAcquireYear = db.Column(db.Integer)
	DateAcquireMonth = db.Column(db.Integer)
	DateAcquireDay = db.Column(db.Integer)
	AccuracyAcquire = db.Column(db.Enum('documented', 'accurate', 'likely'))
	description = db.Column(db.Text)
	Type = db.Column(db.Enum('letter', 'postcard'))

	Heir = db.Column(db.Integer, db.ForeignKey("FamilyMember.FamilyMemberID"))
	CurrentOwner = db.Column(db.Integer, db.ForeignKey("FamilyMember.FamilyMemberID"), nullable=False)

"""
Note that all attribute values for letters and Postcards so that their values and be accessed by the same
command.
"""
class Letter(db.Model):
	__tablename__ = 'Letter'

	Aerogramme = db.Column(db.Boolean, nullable = False)
	Telegram = db.Column(db.Boolean, nullable = False)
	LetterID = db.Column(db.Integer, primary_key = True)
	SenderAddress = db.Column(db.String(100))
	ReceiverAddress = db.Column(db.String(100))
	Sender = db.Column(db.String(45))
	Receiver = db.Column(db.String(45))
	Envelope = db.Column(db.BLOB)
	Artifact_ArtifactID = db.Column(db.Integer, db.ForeignKey('Artifact.ArtifactID'), primary_key = True)

class PostCard(db.Model):
	__tablename__ = 'PostCard'

	PostCardID = db.Column(db.Integer, primary_key = True)
	SenderAddress = db.Column(db.String(45))
	ReceiverAddress = db.Column(db.String(45))
	Sender = db.Column(db.String(45))
	Receiver = db.Column(db.String(45))
	CoverPicture = db.Column(db.BLOB)
	Artifact_ArtifactID = db.Column(db.Integer, db.ForeignKey('Artifact.ArtifactID'), primary_key = True)


"""
Table for artifact images
"""
class ArtifactImage(db.Model):
	__tablename__ = 'ArtifactImage'

	ArtifactImageID = db.Column(db.Integer, primary_key = True)
	Image = db.Column(db.BLOB, nullable = False)
	Caption = db.Column(db.Text)
	Artifact_ArtifactID = db.Column(db.Integer, db.ForeignKey('Artifact.ArtifactID'), nullable = False)


"""
Table for the comments
"""
class Comment(db.Model):
	__tablename__ = 'Comment'

	CommentID = db.Column(db.Integer, primary_key = True)
	Comment = db.Column(db.Text)
	ArtifactID = db.Column(db.Integer, db.ForeignKey('Artifact.ArtifactID'), nullable = False)
	name = db.Column(db.String(45))


"""
Entity table
"""
class Entity(db.Model):
	__tablename__ = 'Entity'

	EntityID = db.Column(db.Integer, primary_key = True)
	Name = db.Column(db.String(45))
	Type = db.Column(db.String(45))
	Tag = db.Column(db.String(45))
	Artifact_ArtifactID = db.Column(db.Integer, db.ForeignKey('Artifact.ArtifactID'), nullable = False)


"""
Entity-person relationship table
"""
class Entity_has_FamilyMember(db.Model):
	__tablename__ = 'Entity_has_FamilyMember'

	Entity_EntityID = db.Column(db.Integer, db.ForeignKey('Entity.EntityID'), primary_key = True)
	FamilyMember_FamilyMemberID = db.Column(db.Integer, db.ForeignKey('FamilyMember.FamilyMemberID'), primary_key = True)