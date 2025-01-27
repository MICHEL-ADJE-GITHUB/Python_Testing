import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for, send_from_directory


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html',clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        competitions_with_valid_date = []
        competitions_done = []
        for comp in competitions:
            date_str = str(comp['date'])
            date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date_object > datetime.datetime.now():
                comp['date'] = date_object
                competitions_with_valid_date.append(comp)
            else:
                competitions_done.append(comp)
        # Pour chaque élément club dans la liste clubs, si le champ email de l'élément club est égal 
        # à la valeur du champ email du formulaire de la requête (request.form['email'])
        # Si cette condition est vraie, l'élément club est ajouté à la nouvelle liste 
        # Enfin, la variable club est assignée à l'élément de la nouvelle liste en utilisant l'index 0 ([0]) pour sélectionner le premier élément de la liste.
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions_with_valid_date,competition_done=competitions_done)
    except IndexError:
        erreur = 1
        return render_template('index.html',erreur=erreur,clubs=clubs)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0] #<---exception here
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
    except:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        competitions_with_valid_date = []
        competitions_done = []

        for comp in competitions:
            date_str = str(comp['date'])
            date_object = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date_object > datetime.datetime.now():
                comp['date'] = date_object
                competitions_with_valid_date.append(comp)
            else:
                competitions_done.append(comp)

        places = request.form.get('places')

        if places:
            placesRequired = int(places)
            if (placesRequired <= int(competition['numberOfPlaces']) and placesRequired > 0) and (int(club['points'])>0 and (int(club['points']) >= placesRequired and placesRequired < 13)):
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - placesRequired
                flash('Felicitation! vous venez de reserver {} places'.format(placesRequired))
            else:
                flash('echec lors de la reservation de {} places !'.format(placesRequired))
        else:
            flash('Aucune place n\'a été sélectionnée!')
        return render_template('welcome.html', club=club, competitions=competitions_with_valid_date, competition_done=competitions_done)
    except Exception as e:
         print(e)
    


@app.route('/images/<path:filename>')
def images(filename):
    try:
        return send_from_directory('images/', filename)
    except Exception as e:
        print(e)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))