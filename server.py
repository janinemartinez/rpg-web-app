"""Movie Ratings."""

from jinja2 import StrictUndefined
import json
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import (
    User, 
    Character,
    Attribute,
    Skill,
    Template,
    Spell,
    Char_spell,
    Char_species,
    Char_skill,
    Class_spell,
    connect_to_db,
    db,
)
import random
# import helper

app = Flask(__name__)

app.secret_key = "POOP"

app.jinja_env.undefined = StrictUndefined

def modifiers(attribute):

    return attribute//2-5


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
    char_align = request.form.get('char_align')





    return render_template("builds_character.html", user_id=user_id, template_id=template_id, spec_id=spec_id, 
        char_name=char_name, flavor_txt=flavor_txt, age=age, char_align=char_align)



@app.route('/builds_character', methods=["POST"])
def add_attributes():

    age = int(request.form.get('age'))
    char_align = request.form.get('char_align')
    character_level = int(request.form.get('character_level'))
    char_name = request.form.get('char_name')
    charisma = request.form.get('charisma')
    constitution = int(request.form.get('constitution'))
    dexterity = request.form.get('dexterity')
    experience_points = int(request.form.get('experience_points'))
    flavor_txt = request.form.get('flavor_txt')
    hit_points = request.form.get('hit_points')
    intelligence = request.form.get('intelligence')
    spec_id = int(request.form.get('spec_id'))
    strength = request.form.get('strength')
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))
    wisdom = request.form.get('wisdom')

    hitdice = Template.query.filter_by(template_id=template_id).first()
    hitdice = hitdice.hit_dice
    first_roll = random.randint(1, hitdice)
    second_roll = random.randint(1, hitdice)

    mod = modifiers(constitution)

    if first_roll >= second_roll:
        hit_points = first_roll + mod
    else:
        hit_points = second_roll + mod

    return render_template("dependencies.html", user_id=user_id, template_id=template_id, spec_id=spec_id,
        char_name=char_name, flavor_txt=flavor_txt, age=age, strength=strength, char_align=char_align,
        dexterity=dexterity, constitution=constitution, intelligence=intelligence, hit_points=hit_points,
        wisdom=wisdom, charisma=charisma, experience_points=experience_points, character_level=character_level, 
        first_roll=first_roll, second_roll=second_roll, mod=mod, hitdice=hitdice)


@app.route('/dependencies', methods=["POST"])
def factor_hp():

    age = int(request.form.get('age'))
    char_align = request.form.get('char_align')
    character_level = int(request.form.get('character_level'))
    char_name = request.form.get('char_name')
    charisma = request.form.get('charisma')
    constitution = int(request.form.get('constitution'))
    dexterity = request.form.get('dexterity')
    experience_points = int(request.form.get('experience_points'))
    flavor_txt = request.form.get('flavor_txt')
    hit_points = request.form.get('hit_points')
    intelligence = request.form.get('intelligence')
    spec_id = int(request.form.get('spec_id'))
    strength = request.form.get('strength')
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))
    wisdom = request.form.get('wisdom')




    return render_template("commit_char.html", age=age, char_align=char_align, character_level=character_level, 
        char_name=char_name, charisma=charisma, constitution=constitution, dexterity=dexterity, 
        experience_points=experience_points, flavor_txt=flavor_txt, intelligence=intelligence, spec_id=spec_id, 
        strength=strength, template_id=template_id, user_id=user_id, wisdom=wisdom, hit_points=hit_points)


@app.route('/commit_char', methods=["POST"])
def commit_char_attr():

    age = int(request.form.get('age'))
    char_align = request.form.get('char_align')
    character_level = int(request.form.get('character_level'))
    char_name = request.form.get('char_name')
    charisma = request.form.get('charisma')
    constitution = request.form.get('constitution')
    dexterity = request.form.get('dexterity')
    experience_points = int(request.form.get('experience_points'))
    flavor_txt = request.form.get('flavor_txt')  
    hit_points = request.form.get('hit_points')
    intelligence = request.form.get('intelligence')
    spec_id = int(request.form.get('spec_id'))
    strength = request.form.get('strength')
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))
    wisdom = request.form.get('wisdom')


    attributes = Attribute(strength=strength, dexterity=dexterity, constitution=constitution, wisdom=wisdom, intelligence=intelligence, charisma=charisma)

    db.session.add(attributes)
    db.session.flush()

    attrib = db.session.query(Attribute).order_by(Attribute.attributes_id.desc()).first()

    attributes_id = attrib.attributes_id

    character = Character(user_id=user_id, char_align=char_align, hit_points=hit_points, template_id=template_id, 
        spec_id=spec_id, char_name=char_name, flavor_txt=flavor_txt, age=age, experience_points=experience_points,
        character_level=character_level, attributes_id=attributes_id)

    db.session.add(character)
    db.session.flush()

    char = db.session.query(Character).order_by(Character.char_id.desc()).first()

    db.session.commit()

    temp_stuff = db.session.query(Template.template_id).first()
    temp = temp_stuff


    flash('Character successfully saved')

    return render_template("add_spells", temp=temp) 



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