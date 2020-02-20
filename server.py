"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Character, Template, Spell, Char_species
import helper

app = Flask(__name__)

app.secret_key = "POOP"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if not User.query.filter_by(email=email).first():
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

    else:
        return redirect('/')
        #placeholder

    return redirect('/')


@app.route('/character_start')
def start_making_character():

    temp_nfo = db.session.query(Template.template_id, Template.template_name).all()

    spec_nfo = db.session.query(Char_species.spec_id, Char_species.spec_type).all()

    return render_template("character_start.html", temp_nfo=temp_nfo, spec_nfo=spec_nfo)

@app.route('/character_start' methods=["POST"])
def first_form():
    character = Character(user_id=user_id, template_id=template_id, spec_id=spec_id, 
        char_name=char_name, flavor_txt=flavor_txt, char_age=char_age)








@app.route('/builds_character' methods=["POST"])
def second_form():

    return render_template("builds_character")


@app.route('/log_in', methods=["GET"])
def log_in():

    return render_template("log_in.html")

@app.route('/log_in', methods=["POST"])
def log_in_form():
    email = request.form.get('email')
    password = request.form.get('password')

    db_user = User.query.filter_by(email=email).first()
    db_password = db_user.password

    if password == db_password:
        session['user_id'] = db_user.user_id
        flash('You were successfully logged in.')
        return redirect('/')

    else:
        flash('Incorrect username or password.')
        return redirect('/log_in')


@app.route('/log_out', methods=["GET"])
def log_out():    
    del session['user_id']
    flash('User logged out.')
    print(session)
    return redirect('/')


if __name__ == "__main__":

    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0", debug=True)