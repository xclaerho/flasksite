from flask import render_template, request, session, redirect, flash, url_for, make_response
from flask_mail import Message
from vermeylen import app, mail, bcrypt
from vermeylen.decorators import *
from vermeylen.models import *
from vermeylen.forms import *
from threading import Thread
import string, random, json, csv, io

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/praesidium')
def praesidium():
    return render_template('praesidium.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/clublied')
def clublied():
    return render_template('clublied.html')

@app.route('/archief')
def archief():
    return render_template('archief.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username', None):
        # user already logged in
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            session['roles'] = user.roles.strip().split(',')
            flash('Succesvol ingelogd.', category='primary')
            return redirect('/')
        else:
            flash('Niet ingelogd. Gelieve uw gebruikersnaam en wachtwoord te controleren.', category="danger")
    return render_template('login.html', login_form=form)

@app.route('/tools')
@login_required
@requires_one_of_roles("tools")
def tools():
    num_inputs = len(Input.query.all())
    return render_template('tools.html', num_inputs=num_inputs)

# Schachten
@app.route('/schachten', methods=['GET', 'POST'])
@login_required
@requires_one_of_roles("tools")
def schachten():
    schachten = Schacht.query.all()
    # create dictionary with points for every schacht (list comprehension is not possible in template)
    points = dict()
    for schacht in schachten:
        points[schacht.id] = sum([task.points for task in schacht.tasks])
    schacht_form = SchachtForm()
    if schacht_form.validate_on_submit():
        new_schacht = Schacht(name=schacht_form.name.data)
        db.session.add(new_schacht)
        db.session.commit()
        flash('Schacht toegevoegd.',category='primary')
        return redirect(url_for('schachten'))
    return render_template('/schachten/admin.html', schachten=schachten, schacht_form=schacht_form,points=points)

@app.route('/exportschachten', methods=['GET'])
@login_required
@requires_one_of_roles("tools")
def schachten_export():
    si = io.StringIO()
    cw = csv.writer(si,dialect=csv.excel)
    schachten = Schacht.query.all()
    for schacht in schachten:
        row = [schacht.name + ' (' + str(sum([task.points for task in schacht.tasks])) + ' punten)' ]
        row.extend([task.name + ' ('+str(task.points)+')' for task in schacht.tasks])
        cw.writerow(row)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/schachten/<id>', methods=['GET','POST'])
@login_required
@requires_one_of_roles("schachten")
def schachten_update(id):
    schacht = Schacht.query.get_or_404(id)
    schacht_form = SchachtForm()
    if schacht_form.validate_on_submit():
        schacht.name = schacht_form.name.data
        db.session.commit()
        flash('Schacht bijgewerkt.',category="primary")
        return redirect(url_for('schachten_update',id=id))
    schacht_form.name.data = schacht.name
    return render_template('/schachten/update.html', schacht=schacht, schacht_form=schacht_form)

@app.route('/schachten/<schacht_id>/opdracht/<task_id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("schachten")
def schachten_remove_task(schacht_id, task_id):
    schacht = Schacht.query.get_or_404(schacht_id)
    task = SchachtenOpdracht.query.get_or_404(task_id)
    schacht.tasks.remove(task)
    db.session.commit()
    return redirect(url_for('schachten_update',id=schacht_id))

@app.route('/schachten/<id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("schachten")
def schachten_delete(id):
    schacht = Schacht.query.get_or_404(id)
    db.session.delete(schacht)
    db.session.commit()
    flash('Schacht verwijderd.', category='primary')
    return redirect(url_for('schachten'))

@app.route('/opdrachten', methods=['GET', 'POST'])
@login_required
@requires_one_of_roles("schachten")
def schachtenopdrachten():
    opdrachten = SchachtenOpdracht.query.all()
    opdracht_form = SchachtenOpdrachtForm()
    if opdracht_form.validate_on_submit():
        new_opdracht = SchachtenOpdracht(name=opdracht_form.name.data,points=opdracht_form.points.data,description=opdracht_form.description.data)
        for id in opdracht_form.schachten.data:
            schacht = Schacht.query.filter_by(id=id).first()
            new_opdracht.schachten.append(schacht)
        db.session.add(new_opdracht)
        db.session.commit()
        flash('Opdracht toegevoegd.',category='primary')
        return redirect(url_for('schachtenopdrachten'))
    return render_template('/schachten/opdrachten.html', opdrachten=opdrachten,opdracht_form=opdracht_form)

@app.route('/opdrachten/<id>', methods=['GET','POST'])
@login_required
@requires_one_of_roles("schachten")
def schachtenopdrachten_update(id):
    opdracht = SchachtenOpdracht.query.get_or_404(id)
    opdracht_form = SchachtenOpdrachtForm()
    if opdracht_form.validate_on_submit():
        opdracht.name = opdracht_form.name.data
        opdracht.points = opdracht_form.points.data
        opdracht.description = opdracht_form.description.data
        opdracht.schachten.clear()
        for schacht_id in opdracht_form.schachten.data:
            schacht = Schacht.query.filter_by(id=schacht_id).first()
            opdracht.schachten.append(schacht)
        db.session.commit()
        flash('Opdracht bijgewerkt.',category='primary')
        return redirect(url_for('schachtenopdrachten_update',id=id))
    opdracht_form.name.data = opdracht.name
    opdracht_form.points.data = opdracht.points
    opdracht_form.description.data = opdracht.description
    opdracht_form.schachten.data = [schacht.id for schacht in opdracht.schachten]
    return render_template('/schachten/opdracht_update.html',opdracht=opdracht,opdracht_form=opdracht_form)

@app.route('/opdrachten/<id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("schachten")
def schachtenopdrachten_delete(id):
    opdracht = SchachtenOpdracht.query.get_or_404(id)
    db.session.delete(opdracht)
    db.session.commit()
    flash('Opdracht verwijderd.',category='primary')
    return redirect(url_for('schachtenopdrachten'))

# Inputs
@app.route('/input', methods=['GET', 'POST'])
def input():
    input_form = InputForm()
    if input_form.validate_on_submit():
        new_input = Input(input=input_form.input.data)
        db.session.add(new_input)
        db.session.commit()
        flash('Bedankt voor de feedback!', category="primary")
        msg = Message(subject='[site] Nieuwe input',sender='noreply.vermeylen@gmail.com', recipients=['homeraadvermeylen@gmail.com'],body=input_form.input.data)
        Thread(target=send_async_email, args=(app, msg)).start()
        return redirect(url_for('input'))
    return render_template('/inputs/input.html', input_form=input_form)

@app.route('/inputs')
@login_required
@requires_one_of_roles("tools")
def inputs():
    inputs = Input.query.all()
    return render_template('/inputs/admin.html', inputs=inputs)

@app.route('/inputs/<id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("tools")
def inputs_delete(id):
    input = Input.query.filter_by(id=id).first()
    db.session.delete(input)
    db.session.commit()
    flash('Input verwijderd.', category='primary')
    return redirect(url_for('inputs'))

# Users (and poef because related to users)
@app.route('/users', methods=['GET', 'POST'])
@login_required
@requires_one_of_roles("gebruikers")
def users():
    users = User.query.all()
    user_form = UserForm()
    if user_form.validate_on_submit():
        user = User(username=user_form.username.data, password=bcrypt.generate_password_hash(user_form.password.data).decode('utf-8'), fullname=user_form.fullname.data, roles=user_form.roles.data)
        db.session.add(user)
        db.session.commit()
        flash('Gebruiker aangemaakt.',category="primary")
        return redirect(url_for('users'))
    return render_template('/users/admin.html', users=users, user_form=user_form)

@app.route('/users/<id>', methods=['GET', 'POST'])
@login_required
@requires_one_of_roles("gebruikers")
def users_update(id):
    user = User.query.get_or_404(id)
    usernameform = UserUsernameForm()
    passwordform = UserPasswordForm()
    rolesform = UserRolesForm()
    # check which form was submitted and validate if submitted
    if usernameform.submitusername.data and usernameform.validate_on_submit():
        oldusername = user.username
        user.username = usernameform.username.data
        db.session.commit()
        if oldusername == session['username']:
            # changing self through praesidium tools
            session['username'] = usernameform.username.data
        flash('Gebruikersnaam bijgewerkt.',category='primary')
    if passwordform.submitpassword.data and passwordform.validate_on_submit():
        user.password = bcrypt.generate_password_hash(passwordform.password.data).decode('utf-8')
        db.session.commit()
        passwordform.password.data = ''
        flash('Wachtwoord bijgewerkt.',category='primary')
    if rolesform.submitroles.data and rolesform.validate_on_submit():
        user.roles = rolesform.roles.data
        db.session.commit()
        flash('Rollen bijgewerkt.',category='primary')
    usernameform.username.data = user.username
    rolesform.roles.data = user.roles
    return render_template('/users/update.html',user=user,usernameform=usernameform,passwordform=passwordform,rolesform=rolesform)

@app.route('/user/<id>/delete', methods=['POST'])
@login_required
def users_delete(id):
    """Self-delete trough profile page or delete through users admin page."""
    user = User.query.get_or_404(id)
    # allow only self-delete or gebruikers role
    if not user.username == session.get('username',None) and 'gebruikers' not in session.get('roles',None):
        flash('Niet toegelaten.',category='danger')
        return redirect(url_for('home'))
    # check if there is still a poef that needs to be paid
    poef = 0
    transactions = PoefTransaction.query.filter_by(user_id=id).all()
    for transaction in transactions:
        poef += transaction.amount
    if poef != 0:
        flash('Openstaande poef moet eerst vereffend worden.',category='danger')
        if user.username == session.get('username',None):
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('users_update',id=id))
    # check if self-delete
    if user.username == session.get('username',None):
        session.clear()
    db.session.delete(user)
    db.session.commit()
    flash('Gebruiker verwijderd.', category="primary")
    return redirect(url_for('users'))

@app.route('/profiel', methods=['GET','POST'])
@login_required
def profile():
    user = User.query.filter_by(username=session.get('username',None)).first()
    transactions = PoefTransaction.query.filter_by(user_id=user.id).all()
    poef = 0
    for transaction in transactions:
        poef += transaction.amount
    poef /= 100
    usernameform = UserUsernameForm()
    passwordform = UserPasswordForm()
    # check which form was submitted and validate if submitted
    if usernameform.submitusername.data and usernameform.validate_on_submit():
        user.username = usernameform.username.data
        db.session.commit()
        session['username'] = usernameform.username.data
        flash('Gebruikersnaam bijgewerkt.',category='primary')
    if passwordform.submitpassword.data and passwordform.validate_on_submit():
        user.password = bcrypt.generate_password_hash(passwordform.password.data).decode('utf-8')
        db.session.commit()
        passwordform.password.data = ''
        flash('Wachtwoord bijgewerkt.',category='primary')
    usernameform.username.data=user.username
    return render_template('/users/profile.html', user=user,transactions=transactions,poef=poef,usernameform=usernameform,passwordform=passwordform)

@app.route('/poef')
@login_required
@requires_one_of_roles("penning")
def users_poef():
    users = User.query.filter(User.roles.contains('poef')).all()
    poef = dict()
    for user in users:
        poef_transactions = PoefTransaction.query.filter_by(user_id=user.id).all()
        debt = 0
        for transaction in poef_transactions:
            debt += transaction.amount
        poef[user.id] = debt/100
    return render_template('/users/poef_overview.html',users=users,poef=poef)

@app.route('/poef/<id>', methods=['GET','POST'])
@login_required
@requires_one_of_roles("penning")
def users_poef_update(id):
    user = User.query.get_or_404(id)
    transactions = PoefTransaction.query.order_by(PoefTransaction.date.desc()).filter_by(user_id=id).all()
    transaction_form = PoefTransactionForm()
    if transaction_form.validate_on_submit():
        # convert amount to cents
        new_transaction = PoefTransaction(amount=int(transaction_form.amount.data*100),description=transaction_form.description.data,user_id=id)
        db.session.add(new_transaction)
        db.session.commit()
        flash('Toegevoegd.',category='primary')
        return redirect(url_for('users_poef_update',id=id))
    return render_template('/users/poef_detail.html',user=user,transactions=transactions,transaction_form=transaction_form)

@app.route('/poef/<user_id>/transaction/<transaction_id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("penning")
def users_poef_delete(user_id,transaction_id):
    transaction = PoefTransaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Verwijderd.',category="primary")
    return redirect(url_for('users_poef_update',id=user_id))

# Augustjes
@app.route('/augustje', methods=['GET', 'POST'])
def augustjes():
    augustjes = Augustje.query.order_by(Augustje.date.desc()).all()
    subscribe_form = AugustjeSubscribeForm()
    if subscribe_form.validate_on_submit():
        subscriber = AugustjeSubscriber(name=subscribe_form.name.data,address=subscribe_form.roomnumber.data)
        db.session.add(subscriber)
        db.session.commit()
        flash('Succesvol geabbonneerd!', category="primary")
        return redirect(url_for('augustjes'))
    return render_template('/augustjes/augustje.html', subscribe_form=subscribe_form, augustjes=augustjes)

@app.route('/augustje/<id>')
def augustjes_read(id):
    augustje = Augustje.query.filter_by(id=id).first()
    return render_template('/augustjes/read.html',augustje=augustje)

@app.route('/augustjes', methods=['GET', 'POST'])
@login_required
@requires_one_of_roles("tools")
def augustjes_admin():
    augustjes = Augustje.query.order_by(Augustje.date.desc()).all()
    augustje_form = AugustjeForm()
    if augustje_form.validate_on_submit():
        augustje = Augustje(name=augustje_form.name.data,embed=augustje_form.embed.data)
        db.session.add(augustje)
        db.session.commit()
        flash('Augustje toegevoegd.',category='primary')
        return redirect(url_for('augustjes_admin'))
    return render_template('/augustjes/admin.html', augustjes=augustjes, augustje_form=augustje_form)

@app.route('/augustjes/<id>', methods=['GET','POST'])
@login_required
@requires_one_of_roles("tools")
def augustjes_update(id):
    augustje = Augustje.query.get_or_404(id)
    augustje_form = AugustjeForm()
    if augustje_form.validate_on_submit():
        augustje.name = augustje_form.name.data
        augustje.embed = augustje_form.embed.data
        db.session.commit()
        flash('Augustje bijgewerkt.',category='primary')
        return redirect(url_for('augustjes_update',id=id))
    augustje_form.name.data = augustje.name
    augustje_form.embed.data = augustje.embed
    return render_template('/augustjes/update.html', augustje=augustje, augustje_form=augustje_form)

@app.route("/augustjes/<id>/delete", methods=["POST"])
@login_required
@requires_one_of_roles("tools")
def augustjes_delete(id):
    augustje = Augustje.query.get_or_404(id)
    db.session.delete(augustje)
    db.session.commit()
    flash('Augustje verwijderd.', category="primary")
    return redirect(url_for('augustjes_admin'))

@app.route('/subscribers')
@login_required
@requires_one_of_roles("tools")
def augustjesubscribers():
    subscribers = AugustjeSubscriber.query.order_by(AugustjeSubscriber.name).all()
    return render_template('/augustjes/subscribers.html', subscribers=subscribers)

@app.route('/subscribers/<id>/delete', methods=['POST'])
@login_required
@requires_one_of_roles("tools")
def augustjesubscribers_delete(id):
    subscriber = AugustjeSubscriber.query.get_or_404(id)
    db.session.delete(subscriber)
    db.session.commit()
    flash('Abonnee verwijderd.',category='primary')
    return redirect(url_for('augustjesubscribers'))

# Muilgraaf
@app.route('/muilgraaf')
@login_required
def muilgraaf():
    people = MuilgraafPerson.query.all()
    links = MuilgraafLink.query.order_by(MuilgraafLink.event.desc()).all()
    person_form = MuilgraafPersonForm()
    link_form = MuilgraafLinkForm()
    return render_template('/muilgraaf/muilgraaf.html', people=people,links=links, person_form=person_form, link_form=link_form)

@app.route('/muilgraaf/person', methods=['POST', 'GET'])
@login_required
def muilgraaf_add_person():
    person_form = MuilgraafPersonForm()
    if person_form.validate_on_submit():
        new_person = MuilgraafPerson(name=person_form.name.data, club=person_form.club.data)
        db.session.add(new_person)
        db.session.commit()
        flash('Persoon toegevoegd.',category='primary')
        return redirect(url_for('muilgraaf'))
    return render_template('/muilgraaf/person_error.html',person_form=person_form)

@app.route('/muilgraaf/person/<id>/delete', methods=['POST', 'GET'])
@login_required
def muilgraaf_delete_person(id):
    person = MuilgraafPerson.query.get_or_404(id)
    links = MuilgraafLink.query.filter_by(person_1=id).all()
    for link in links:
        db.session.delete(link)
    links = MuilgraafLink.query.filter_by(person_2=id).all()
    for link in links:
        db.session.delete(link)
    db.session.delete(person)
    db.session.commit()
    flash('Persoon verwijderd.',category='primary')
    return redirect(url_for('muilgraaf'))

@app.route('/muilgraaf/link/<id>/delete', methods=['POST', 'GET'])
@login_required
def muilgraaf_delete_link(id):
    link = MuilgraafLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    flash('Link verwijderd.',category='primary')
    return redirect(url_for('muilgraaf'))

@app.route('/muilgraaf/link', methods=['POST', 'GET'])
@login_required
def muilgraaf_add_link():
    link_form = MuilgraafLinkForm()
    if link_form.validate_on_submit():
        new_link = MuilgraafLink(person_1=link_form.person_1.data,person_2=link_form.person_2.data,event=link_form.event.data,location=link_form.location.data,description=link_form.description.data)
        db.session.add(new_link)
        db.session.commit()
        flash('Link toegevoegd.',category='primary')
        return redirect(url_for('muilgraaf'))
    return render_template('/muilgraaf/link_error.html',link_form=link_form)

# Voting
@app.route('/elections',methods=['GET','POST'])
@login_required
@requires_one_of_roles("stemmingen")
def elections():
    elections = Election.query.all()
    electionform = ElectionForm()
    if electionform.validate_on_submit():
        new_election = Election(name=electionform.name.data,votesperperson=electionform.votesperperson.data)
        db.session.add(new_election)
        db.session.commit()
        flash('Stemming aangemaakt.',category='primary')
        return redirect(url_for('elections'))
    electionform.votesperperson.data = 1
    return render_template('/voting/admin.html',elections=elections,electionform=electionform)

@app.route('/elections/<id>/toggle-visibility',methods=['POST'])
@login_required
@requires_one_of_roles("stemmingen")
def elections_toggle_visibility(id):
    election = Election.query.get_or_404(id)
    election.open = (election.open+1)%2
    db.session.commit()
    flash('Bijgewerkt.',category='primary')
    return redirect(url_for('elections_update',id=id))

@app.route('/elections/<id>',methods=['GET','POST'])
@login_required
@requires_one_of_roles("stemmingen")
def elections_update(id):
    election = Election.query.get_or_404(id)
    options = election.options
    vote_count = dict()
    for option in options:
        vote_count[option.id] = db.session.query(votes).filter_by(optionid=option.id).count()
    electionform = ElectionForm()
    optionform = ElectionOptionForm()
    if optionform.submitoption.data and optionform.validate_on_submit():
        new_option = ElectionOption(name=optionform.name.data,election_id=id)
        db.session.add(new_option)
        db.session.commit()
        flash('Optie toegevoegd.',category='primary')
        return redirect(url_for('elections_update',id=id))
    if electionform.submitelection.data and electionform.validate_on_submit():
        election.name = electionform.name.data
        election.votesperperson = electionform.votesperperson.data
        db.session.commit()
        flash('Bijgewerkt.',category='primary')
    electionform.name.data = election.name
    electionform.votesperperson.data = election.votesperperson
    return render_template('/voting/update.html',election=election,optionform=optionform,electionform=electionform,options=options,vote_count=vote_count)

@app.route('/elections/<id>/delete',methods=['POST'])
@login_required
@requires_one_of_roles("stemmingen")
def elections_delete(id):
    election = Election.query.get_or_404(id)
    db.session.delete(election)
    db.session.commit()
    flash('Verwijderd.',category='primary')
    return redirect(url_for('elections'))

@app.route('/elections/<electionid>/option/<optionid>/delete',methods=['POST'])
@login_required
@requires_one_of_roles("stemmingen")
def elections_delete_option(electionid,optionid):
    option = ElectionOption.query.get_or_404(optionid)
    db.session.delete(option)
    db.session.commit()
    flash('Optie verwijderd.',category='primary')
    return redirect(url_for('elections_update',id=electionid))

@app.route('/elections/keys',methods=['GET','POST'])
@login_required
@requires_one_of_roles("stemmingen")
def keys():
    if request.method == 'POST':
        valid = False
        while not valid:
            letters = string.ascii_uppercase
            key = ''.join(random.choice(letters) for i in range(15))
            if not VoterKey.query.filter_by(key=key).first():
                valid=True
                new_key = VoterKey(key=key)
                db.session.add(new_key)
                db.session.commit()
                flash('Nieuwe login toegevoegd.',category='primary')
                return redirect(url_for('keys'))
    keys = VoterKey.query.all()
    return render_template('/voting/keys.html',keys=keys)

@app.route('/elections/keys/all/delete',methods=['POST'])
@login_required
@requires_one_of_roles("stemmingen")
def delete_all_keys():
    db.session.query(VoterKey).delete()
    db.session.commit()
    flash('Alle logins verwijderd.',category='primary')
    return redirect(url_for('keys'))

@app.route('/elections/keys/<id>/delete',methods=['POST'])
@login_required
@requires_one_of_roles("stemmingen")
def keys_delete(id):
    key = VoterKey.query.get_or_404(id)
    db.session.delete(key)
    db.session.commit()
    flash('Login verwijderd.',category='primary')
    return redirect(url_for('keys'))

@app.route('/stem',methods=['GET','POST'])
def vote_overview():
    keyform = VoterKeyForm()
    if keyform.submitkey.data and keyform.validate_on_submit():
        # check if valid key
        key = VoterKey.query.filter_by(key=keyform.key.data).first()
        if key:
            session['voterid'] = key.id
            return redirect(url_for('vote_overview'))
        else:
            flash('Login mislukt.',category='danger')
            return redirect(url_for('vote_overview'))
    elections = Election.query.filter_by(open=1).all()
    return render_template('/voting/overview.html',keyform=keyform,elections=elections)

@app.route('/stem/<id>',methods=['GET','POST'])
def vote(id):
    # check if already logged in to voting
    if not session.get('voterid',None):
        return redirect(url_for('vote_overview'))
    # initialize form and check if still votes left for this election
    voteform = VoteForm()
    previous_votes = []
    options = ElectionOption.query.filter_by(election_id=id).all()
    for option in options:
        voteform.option.choices.append((option.id,option.name))
        prev = db.session.query(votes).filter_by(optionid=option.id,voterkey=session.get('voterid')).all()
        previous_votes.extend(prev)
    election = Election.query.get_or_404(id)
    if voteform.validate_on_submit():
        if len(previous_votes) >= election.votesperperson:
            flash('Al max aantal keren gestemd.',category='danger')
            return redirect(url_for('vote_overview'))
        if len([vote for vote in previous_votes if vote.optionid is voteform.option.data]) is 0:
            db.session.execute(votes.insert().values(voterkey=session.get('voterid'),optionid=voteform.option.data))
            db.session.commit()
            flash('Gestemd.',category='primary')
            return redirect(url_for('vote',id=id))
        else:
            flash('Meerdere keren op dezelfde optie stemmen is niet toegelaten.',category='danger')
            return redirect(url_for('vote',id=id))
    return render_template('/voting/stem.html',previous_votes=previous_votes,election=election,voteform=voteform)

# Bar
@app.route('/bar',methods=['GET','POST'])
@login_required
@requires_one_of_roles("tools")
def bar():
    items = BarItem.query.order_by(BarItem.name).all()
    transactions = BarTransaction.query.order_by(BarTransaction.date.desc()).limit(10).all()
    itemform = BarItemForm()
    if itemform.submititem.data and itemform.validate_on_submit():
        new_item = BarItem(name=itemform.name.data,price=int(itemform.price.data*100),amount=itemform.amount.data,category=itemform.category.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Item toegevoegd.',category='primary')
        return redirect(url_for('bar'))
    return render_template('/bar/admin.html',items=items,transactions=transactions,itemform=itemform)

@app.route('/bar/items/<id>',methods=['GET','POST'])
@login_required
@requires_one_of_roles("tools")
def bar_items(id):
    item = BarItem.query.get_or_404(id)
    itemform = BarItemForm()
    if itemform.validate_on_submit():
        item = BarItem.query.get_or_404(id)
        item.name = itemform.name.data
        item.price = int(itemform.price.data*100)
        item.amount = itemform.amount.data
        item.category = itemform.category.data
        db.session.commit()
        flash('Bijgewerkt.',category='primary')
        return redirect(url_for('bar'))
    itemform.name.data = item.name
    itemform.amount.data = item.amount
    itemform.category.data = item.category
    itemform.price.data = item.price/100
    return render_template('/bar/item.html',itemform=itemform,item=item)

@app.route('/bar/items/<id>/delete',methods=['POST'])
@login_required
@requires_one_of_roles("tools")
def bar_items_delete(id):
    item = BarItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item verwijderd.',category='primary')
    return redirect(url_for('bar'))

@app.route('/bar/transaction',methods=['POST'])
@login_required
@requires_one_of_roles("tools")
def bar_transaction():
    data = request.get_json()
    # check if not empty
    if data['price'] == 0:
        return 'Empty order', 204
    order = data['order']
    # update inventory
    for itemid in order:
        item = BarItem.query.get_or_404(itemid)
        item.amount -= order[itemid]['amount']
    # create transaction in db
    new_transaction = BarTransaction(price=data['price'],order=json.dumps(order))
    # add poeftransaction if poef
    if data.get('poef',None):
        poef_transaction = PoefTransaction(amount=data['price'],user_id=data['poef'],description=json.dumps(order))
        db.session.add(poef_transaction)
        db.session.flush()
        new_transaction.poeftransaction = poef_transaction.id
    db.session.add(new_transaction)
    # save all changes
    db.session.commit()
    return "Order added", 200

@app.route('/bar/transaction/<id>/delete',methods=['POST'])
@login_required
@requires_one_of_roles("tools")
def bar_transaction_delete(id):
    transaction = BarTransaction.query.get_or_404(id)
    order = json.loads(transaction.order)
    # undo poef if poeftransaction
    if transaction.poeftransaction:
        # only penning role can undo poef transactions
        if not 'penning' in session['roles']:
            return "Not penning", 403
        poef_transaction = PoefTransaction.query.get_or_404(transaction.poeftransaction)
        db.session.delete(poef_transaction)
    # update inventory back
    for itemid in order:
        item = BarItem.query.filter_by(id=itemid).first()
        # check if item still exists (may be deleted since creation of this transaction)
        if item:
            item.amount += order[itemid]['amount']
    # delete transaction
    db.session.delete(transaction)
    # commit all changes
    db.session.commit()
    flash('Verwijderd.',category='primary')
    return redirect(url_for('bar'))

@app.route('/bar/kassa')
@login_required
@requires_one_of_roles("tools")
def bar_kassa():
    items = BarItem.query.order_by(BarItem.name).all()
    poef_users = User.query.order_by(User.fullname).filter(User.roles.contains('poef'))
    return render_template('/bar/kassa.html', poef_users=poef_users,items=items)