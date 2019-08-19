from datetime import datetime
from vermeylen import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 60 char password because Bcrypt is 60 characters long
    password = db.Column(db.String(60), nullable=False)
    fullname = db.Column(db.String(70), nullable=False)
    # Comma seperated list of roles
    roles = db.Column(db.String(), default="")

class PoefTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Stored in cents to avoid floating point errors
    amount = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.now)
    user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    description = db.Column(db.String)

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Augustje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    embed = db.Column(db.String, nullable=False)

class AugustjeSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    address = db.Column(db.String, nullable=False)

# Table to link schachten with schachtenopdrachten
fulfilled = db.Table('fulfilled',
    db.Column('schacht_id', db.Integer, db.ForeignKey('schacht.id')),
    db.Column('opdracht_id', db.Integer, db.ForeignKey('schachten_opdracht.id'))
    )

class Schacht(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    tasks = db.relationship('SchachtenOpdracht', secondary=fulfilled, backref=db.backref('schachten'))

class SchachtenOpdracht(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    description = db.Column(db.String)

class MuilgraafPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    club = db.Column(db.String(30))

class MuilgraafLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_1 = db.Column(db.Integer, db.ForeignKey('muilgraaf_person.id'), nullable=False)
    person_2 = db.Column(db.Integer, db.ForeignKey('muilgraaf_person.id'), nullable=False)
    event = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String)
    description = db.Column(db.String)

votes = db.Table('votes',
    db.Column('voterkey', db.Integer, db.ForeignKey('voter_key.id')),
    db.Column('electionid', db.Integer, db.ForeignKey('election.id')),
    db.Column('optionid', db.Integer, db.ForeignKey('election_option.id'))
    )

class VoterKey(db.Model):
    """Used to log in to the voting."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(15), nullable=False)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    open = db.Column(db.Integer, default=0)
    votesperperson = db.Column(db.Integer,nullable=False, default=1)

class ElectionOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70),nullable=False)
    election = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)

class BarTransaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.now)
    # Price in cents to avoid floating point errors
    price = db.Column(db.Integer)
    # JSON string version of order
    order = db.Column(db.String,nullable=False)
    poeftransaction = db.Column(db.Integer, db.ForeignKey('poef_transaction.id'))

class BarItem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(70),nullable=False)
    # stored in cents to avoid floating point errors
    price = db.Column(db.Integer,nullable=False)
    # total amount and amount upstairs
    amount = db.Column(db.Integer,default=0)
    category = db.Column(db.String(70))