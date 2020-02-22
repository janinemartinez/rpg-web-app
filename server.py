"""Movie Ratings."""

from jinja2 import StrictUndefined
import json
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Character, Template, Spell, Char_species
# import helper

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

@app.route('/character_start', methods=["POST"])
def first_form():
    assert 'user_id' in session

    char_name = request.form.get('char_name')
    template_id = request.form.get('template_id')
    spec_id = request.form.get('spec_id')
    flavor_txt = request.form.get('flavor_txt')
    age = request.form.get('age')
    user_id = session.get('user_id')





    return render_template("builds_character.html", user_id=user_id, template_id=template_id, spec_id=spec_id, 
        char_name=char_name, flavor_txt=flavor_txt, age=age)



@app.route('/builds_character', methods=["POST"])
def add_attributes():

    char_name = request.form.get('char_name')
    template_id = request.form.get('template_id')
    spec_id = request.form.get('spec_id')
    flavor_txt = request.form.get('flavor_txt')
    age = request.form.get('age')
    user_id = request.form.get('user_id')
    strength = request.form.get('strength')
    dexterity = request.form.get('dexterity')
    constitution = request.form.get('constitution')
    intelligence = request.form.get('intelligence')
    wisdom = request.form.get('wisdom')
    charisma = request.form.get('charisma')
    character_level = int(request.form.get('character_level'))
    experience_points = int(request.form.get('experience_points'))


    # asi = Char_species.query.get(spec_id)
    # bonus = json.loads(asi.spec_stat_mod)
    # bonus = bonus[0]

    return render_template("dependencies.html", user_id=user_id, template_id=template_id, spec_id=spec_id,
        char_name=char_name, flavor_txt=flavor_txt, age=age, strength=strength,
        dexterity=dexterity, constitution=constitution, intelligence=intelligence,
        wisdom=wisdom, charisma=charisma, experience_points=experience_points, character_level=character_level)


@app.route('/dependencies', methods=["POST"])
def upload_char():

    char_name = request.form.get('char_name')
    template_id = int(request.form.get('template_id'))
    spec_id = int(request.form.get('spec_id'))
    flavor_txt = request.form.get('flavor_txt')
    age = int(request.form.get('age'))
    user_id = int(request.form.get('user_id'))
    strength = request.form.get('strength')
    dexterity = request.form.get('dexterity')
    constitution = request.form.get('constitution')
    intelligence = request.form.get('intelligence')
    wisdom = request.form.get('wisdom')
    charisma = request.form.get('charisma')
    character_level = int(request.form.get('character_level'))
    experience_points = int(request.form.get('experience_points'))
    num_skills = 3
    hit_points = 9


    character = Character(user_id=user_id, hit_points=hit_points, num_skills=num_skills, template_id=template_id, spec_id=spec_id,
        char_name=char_name, flavor_txt=flavor_txt, age=age, experience_points=experience_points, character_level=character_level)
    db.session.add(character)
    db.session.commit()

    flash('Character successfully saved')
    return redirect('/')
    # return render_template("bonuses.html", user_id=user_id, template_id=template_id, spec_id=spec_id,
    #     char_name=char_name, flavor_txt=flavor_txt, age=age, strength=strength,
    #     dexterity=dexterity, constitution=constitution, intelligence=intelligence,
    #     wisdom=wisdom, charisma=charisma, experience_points=experience_points, character_level=character_level)


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