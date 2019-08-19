from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, TextAreaField, SelectMultipleField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError
from vermeylen.models import User, Schacht, MuilgraafPerson

class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(message="Verplicht."), Length(min=2, max=20, message="Een gebruikersnaam moet tussen de 2 en 20 karakters lang zijn.")])
    password = PasswordField('Wachtwoord', validators=[DataRequired(message="Verplicht.")])
    submit = SubmitField('Login')

class AugustjeSubscribeForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(message="Verplicht."), Length(min=2,max=70,message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    roomnumber = StringField('Kamernummer/adres', validators=[DataRequired(message="Verplicht.")])
    accept = BooleanField('Ik accepteer dat Home Vermeylen deze gegevens bewaart tot het begin van het volgende academiejaar.', validators=[DataRequired(message="Verplicht.")])
    submit = SubmitField('Verstuur')

class InputForm(FlaskForm):
    input = TextAreaField('Input', validators=[DataRequired(message="Verplicht.")])
    submit = SubmitField('Verstuur')

class AugustjeForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired(message="Verplicht."), Length(min=2, max=20, message="Gelieve een naam tussen 2 en 20 karakters lang in te geven.")])
    embed = StringField('Embed code', validators=[DataRequired("Verplicht.")])
    submit = SubmitField('Verstuur')

class UserForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(message="Verplicht."), Length(min=2, max=20, message="Een gebruikersnaam moet tussen de 2 en 20 karakters lang zijn.")])
    password = StringField('Initieel wachtwoord', validators=[DataRequired(message="Verplicht.")])
    fullname = StringField('Volledige naam', validators=[DataRequired(message="Verplicht."), Length(min=2,max=70,message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    roles = StringField('Rollen')
    submit = SubmitField('Verstuur')

    def validate_username(self, field):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Gebruikersnaam al in gebruik.')

class UserUsernameForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(message="Verplicht."), Length(min=2, max=20, message="Een gebruikersnaam moet tussen de 2 en 20 karakters lang zijn.")])
    submitusername = SubmitField('Update')

    def validate_username(self, field):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Gebruikersnaam al in gebruik.')

class UserPasswordForm(FlaskForm):
    password = StringField('Wachtwoord', validators=[DataRequired(message="Verplicht.")])
    submitpassword = SubmitField('Update')

class UserRolesForm(FlaskForm):
    roles = StringField('Rollen')
    submitroles = SubmitField('Update')

class PoefTransactionForm(FlaskForm):
    amount = DecimalField('Bedrag',validators=[DataRequired(message='Verplicht. Gebruik een punt voor kommagetallen.')])
    description = StringField('Beschrijving')
    submit = SubmitField('Verstuur')

class SchachtForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(message='Verplicht.'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    submit = SubmitField('Verstuur')

class SchachtenOpdrachtForm(FlaskForm):
    name = StringField('Opdracht',validators=[DataRequired(message='Verplicht.'),Length(min=2,max=50,message="Gelieve een naam tussen 2 en 50 karakters lang in te geven.")])
    points = IntegerField('Punten',validators=[DataRequired(message='Verplicht.')])
    description = TextAreaField('Beschrijving')
    schachten = SelectMultipleField('Schachten',validators=[DataRequired(message='Minstens 1 schacht kiezen.')],coerce=int)
    submit = SubmitField('Verstuur')

    def __init__(self, *args, **kwargs):
        super(SchachtenOpdrachtForm, self).__init__(*args, **kwargs)
        self.schachten.choices = [(a.id, a.name) for a in Schacht.query.order_by(Schacht.name)]

class MuilgraafPersonForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(message='Verplicht.'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    club = StringField('Club',validators=[Length(max=30, message="Gelieve een naam van maximaal 30 karakters lang in te geven.")])
    submit = SubmitField('Verstuur')

class MuilgraafLinkForm(FlaskForm):
    person_1 = SelectField('Persoon 1',validators=[DataRequired('Verplicht.')],coerce=int)
    person_2 = SelectField('Persoon 2',validators=[DataRequired('Verplicht.')],coerce=int)
    event = SelectField('Wat?',coerce=int,validators=[DataRequired(message='Verplicht.')],choices=[(1, 'Gemuild'),(2, 'Seks'),(3, 'Relatie')])
    location = StringField('Locatie')
    description = TextAreaField('Extra info')
    submit = SubmitField('Verstuur')

    def __init__(self, *args, **kwargs):
        super(MuilgraafLinkForm, self).__init__(*args, **kwargs)
        people = MuilgraafPerson.query.order_by(MuilgraafPerson.name)
        self.person_1.choices = [(a.id, a.name+" ("+a.club+")" if a.club else a.name) for a in people]
        self.person_2.choices = [(a.id, a.name+" ("+a.club+")" if a.club else a.name) for a in people]
    
    def validate_person_2(self, field):
        if field.data == self.person_1.data:
            raise ValidationError('Gelieve 2 verschillende personen te kiezen.')

class ElectionForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(message='Verplicht.'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    votesperperson = IntegerField('Stemmen per persoon',validators=[DataRequired(message='Verplicht')])
    submitelection = SubmitField('Verstuur')

class ElectionOptionForm(FlaskForm):
    name = StringField('Nieuwe optie',validators=[DataRequired(message='Verplicht.'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    submitoption = SubmitField('Verstuur')

class VoterKeyForm(FlaskForm):
    key = StringField('',validators=[DataRequired(message='Verplicht.')])
    submitkey = SubmitField('Login')

class VoteForm(FlaskForm):
    option = SelectField('',validators=[DataRequired(message='Verplicht.')],choices=[],coerce=int)
    submitvote = SubmitField('Stem')

class BarItemForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(message='Verplicht'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    price = DecimalField('Bedrag',validators=[DataRequired(message='Verplicht. Gebruik een punt voor kommagetallen.')])
    amount = IntegerField('Aantal',validators=[DataRequired(message='Verplicht.')])
    category = StringField('Categorie',validators=[DataRequired(message='Verplicht'),Length(min=2,max=70, message="Gelieve een naam tussen 2 en 70 karakters lang in te geven.")])
    submititem = SubmitField('Verstuur')