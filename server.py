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

def if_spells(dct):
    for item in range(0, 21):
        try:
            if dct.get(f'{item}'):
                return True
        except AttributeError:
            continue
    return False

def how_many_spells(lst):

    num_levels = 0
    dif_levels = []

    for i in lst:
        if i[0] in dif_levels:
            continue
        else:
            dif_levels.append(i[0])
            num_levels += 1

    return list(range(num_levels)), dif_levels

def growth_lst(dict):

    iters=0
    growth_list = []

    for key in dict:
        for rnge in range((dict[key])):
            growth_list.append((iters, int(key)))
            iters+=1
    return growth_list

def compliment_list(last, num):

    return list(range((last[-1]+1), num))

def commit_spell(spell_array, char):

    for spell in spell_array:
        if int(spell) < 1:
            continue
        else:    
            spell_obj=Char_spell(char_id=char, spell_id=spell)
            db.session.add(spell_obj)
    db.session.commit()

def commit_skill(skill_array, char):

    for skill in skill_array:
        if int(skill) < 1:
            continue
        else:    
            skill_obj=Char_skill(char_id=char, skill_id=skill)
            db.session.add(skill_obj)
    db.session.commit()


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
    charisma = int(request.form.get('charisma'))
    constitution = int(request.form.get('constitution'))
    dexterity = int(request.form.get('dexterity'))
    experience_points = int(request.form.get('experience_points'))
    flavor_txt = request.form.get('flavor_txt')  
    hit_points = int(request.form.get('hit_points'))
    intelligence = int(request.form.get('intelligence'))
    spec_id = int(request.form.get('spec_id'))
    strength = int(request.form.get('strength'))
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))
    wisdom = int(request.form.get('wisdom'))

    #creates attribute object
    attributes = Attribute(strength=strength, dexterity=dexterity, constitution=constitution, wisdom=wisdom, intelligence=intelligence, charisma=charisma)

    #adds attrobite object to the session and flushes
    db.session.add(attributes)
    db.session.flush()

    #searches attribute in session to retrieve id
    attrib = db.session.query(Attribute).order_by(Attribute.attributes_id.desc()).first()
    attributes_id = attrib.attributes_id

    #creates character object
    character = Character(user_id=user_id, char_align=char_align, hit_points=hit_points, template_id=template_id, 
        spec_id=spec_id, char_name=char_name, flavor_txt=flavor_txt, age=age, experience_points=experience_points,
        character_level=character_level, attributes_id=attributes_id)

    #commits character object and attribute object to database
    db.session.add(character)
    db.session.commit()

    #retrieves character id
    char = db.session.query(Character).order_by(Character.char_id.desc()).first()
    this_template = Template.query.filter_by(template_id=template_id).first()

    #retrieves the jsons which shows the characters accumulation of spells and special abilities
    growth_item = json.loads(this_template.growth_table)
    growth_item = growth_item[f'{character_level}']


    #nullifies instances where that would cause the user to select spells lest they have no spells to pick
    if "spells_known" in growth_item:
        del growth_item["spells_known"]

    if "bonus_spell" in growth_item:
        del growth_item["bonus_spell"]

    if "Additional Spells" in growth_item:
        del growth_item["Additional Spells"]

    spells = if_spells(growth_item)

    char_id = char.char_id

    if this_template.spell_ability == "null" or spells == False:

        skills = []

        skill_nfo, skills_num = this_template.skill_choices, this_template.num_skills
        skill_info = skill_nfo.rsplit(', ')

        for i in skill_info:
            i = int(i)
            skill_obj = Skill.query.get(i)
            skills.append((skill_obj.skill_id, skill_obj.skill_name))

        num_skills = list(range(1, skills_num+1))
        other_list = compliment_list(num_skills, 6)

        return render_template("add_skills", template_id=template_id, skills=skills, num_skills=num_skills, other_list=other_list, char_id=char_id,
            user_id=user_id)
    else:



        growth_list = growth_lst(growth_item)

        # flash('Character successfully saved')

        spell_objects = db.session.query(Class_spell.template_id, Class_spell.spell_id).all()

        rel_spells = []
        specific_spells = []


        for i in spell_objects:
            if i[0] == template_id:
                rel_spells.append(i[1])

        for i in rel_spells:
            x = Spell.query.get(i)
            if int(x.int_requirement) <= character_level:
                specific_spells.append((x.int_requirement, x.spell_name, x.spell_id))
        

        no_spells=list(range(len(growth_list)))
        unvariety = compliment_list(no_spells, 8)

    return render_template("add_spells", growth_list=growth_list, spell_objects=spell_objects, specific_spells=specific_spells, 
        unvariety=unvariety, template_id=template_id, user_id=user_id, char_id=char_id) 

@app.route('/add_skills_after_spells', methods=["POST"])
def skills_after_spells():

    char_id = int(request.form.get('char_id'))
    spell_id_0 = int(request.form.get('spell_id_0'))
    spell_id_1 = int(request.form.get('spell_id_1'))
    spell_id_2 = int(request.form.get('spell_id_2'))
    spell_id_3 = int(request.form.get('spell_id_3'))
    spell_id_4 = int(request.form.get('spell_id_4'))
    spell_id_5 = int(request.form.get('spell_id_5'))
    spell_id_6 = int(request.form.get('spell_id_6'))
    spell_id_7 = int(request.form.get('spell_id_7'))
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))

    this_template = Template.query.filter_by(template_id=template_id).first()

    skills = []

    skill_nfo, skills_num = this_template.skill_choices, this_template.num_skills
    skill_info = skill_nfo.rsplit(', ')

    for i in skill_info:
        i = int(i)
        skill_obj = Skill.query.get(i)
        skills.append((skill_obj.skill_id, skill_obj.skill_name))

    num_skills = list(range(1, skills_num+1))
    other_list = compliment_list(num_skills, 6)

    spell_ids = [spell_id_0, spell_id_1, spell_id_2, spell_id_3, spell_id_4, spell_id_5, spell_id_6, spell_id_7]
    commit_spell(spell_ids, char_id)

    return render_template("add_skills_after_spells", template_id=template_id, user_id=user_id, 
        char_id=char_id, other_list=other_list, num_skills=num_skills, skills=skills) 

@app.route('/commit_char_true', methods=["POST"])
def commit_show_char():
    
    char_id = int(request.form.get('char_id'))
    skill_id_1 = int(request.form.get('skill_id_1'))
    skill_id_2 = int(request.form.get('skill_id_2'))
    skill_id_3 = int(request.form.get('skill_id_3'))
    skill_id_4 = int(request.form.get('skill_id_4'))
    skill_id_5 = int(request.form.get('skill_id_5'))
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))

    skill_ids = [skill_id_1, skill_id_2, skill_id_3, skill_id_4, skill_id_5]
    commit_skill(skill_ids, char_id)

    return redirect('/')

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