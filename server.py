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

app.secret_key = "tiger&luna"

app.jinja_env.undefined = StrictUndefined

def add_attribute_inc(attrib1, attrib2, stre, dex, con, inte, wis, cha, attribid):

    bonuses = [attrib1, attrib2]

    attributes = Attribute.query.filter_by(attributes_id=attribid).first()

    for i in bonuses:
        if attrib1 == "strength":
            stre += 1
        elif attrib1 == "dexterity":
            dex += 1
        elif attrib1 == "constitution":
            con += 1
        elif attrib1 == "intelligence":
            inte += 1
        elif attrib1 == "wisdom":
            wis += 1
        else:
            cha += 1


    attributes.strength = stre
    attributes.dexterity = dex
    attributes.constitution = con
    attributes.wisdom = wis
    attributes.intelligence=inte
    attributes.charisma=cha

    db.session.add(attributes)
    db.session.commit()

def convert(lst):
    return eval(lst)

def retrieve_char_spells(char_id):

    char_spell_obj = db.session.query(Char_spell.char_id, Char_spell.spell_id)
    char_spell_obj = set(char_spell_obj)

    spells_array = []

    for i in char_spell_obj:
        if i[0] == char_id:
            spells_array.append(i[1])
    return spells_array

def retrieve_spells(spells_array):
    
    spells=[]    
    for spell_id in spells_array:
        spell = Spell.query.filter_by(spell_id=spell_id).all()
        for i in spell:
            spell_desc, spell_name = i.spell_desc, i.spell_name
            spells.append((spell_desc, spell_name))

    return spells

def char_query(charid):

    return Character.query.filter_by(char_id=charid).first()

def template_query(tempid):

    return Template.query.filter_by(template_id=tempid).first()


def retrieve_user_characters(charlst, user):

    user_chars=[]

    for i in charlst:
        if i[2] == user:
            user_chars.append(i)


    # returns char attributes in this order: char_id, char_name, user_id, template_id, spec_id, experience_points, 
    # character_level, attributes_id
    return user_chars

def append_user_characters(chrlst):

    user_chars = []

    for i in chrlst:
        j=list(i)
        template=Template.query.filter_by(template_id=i[3]).first()
        j.append(template.template_name)
        species=Char_species.query.filter_by(spec_id=i[4]).first()
        j.append(species.spec_type)
        user_chars.append(j)

    # returns char attributes in this order: char_id, char_name, user_id, template_id, spec_id, experience_points, 
    # character_level, attributes_id, template_name, spec_name
    return user_chars


def retrieve_char_skills(char_id):

    char_skill_obj = db.session.query(Char_skill.char_id, Char_skill.skill_id)
    char_skill_obj = set(char_skill_obj)

    skills_array = []

    for i in char_skill_obj:
        if i[0] == char_id:
            skills_array.append(i[1])
    return skills_array

def retrieve_skills(skills_array):
    
    skills=[]    
    for skill_id in skills_array:
        skill = Skill.query.filter_by(skill_id=skill_id).all()
        for i in skill:
            skill_desc, skill_name = i.skill_desc, i.skill_name
            skills.append((skill_desc, skill_name))

    return skills

def retrieve_race(spec_id):
    race = Char_species.query.filter_by(spec_id=spec_id).first()
    spec_type = race.spec_type
    speed = race.speed

    return [spec_type, speed]

def retrieve_attributes(attributes_id):

    attributes = Attribute.query.filter_by(attributes_id=attributes_id).first()
    strength = attributes.strength
    dexterity = attributes.dexterity
    constitution = attributes.constitution
    wisdom = attributes.wisdom
    intelligence = attributes.intelligence
    charisma = attributes.charisma

    return [strength, dexterity, constitution, wisdom, intelligence, charisma]

def retrieve_character(char_id):

    character = Character.query.filter_by(char_id=char_id).first()
    name = character.char_name
    char_align = character.char_align
    flavor_txt = character.flavor_txt
    hit_points = character.hit_points
    age = character.age
    experience_points = character.experience_points
    character_level = character.character_level
    spec_id = character.spec_id

    return spec_id, character, [name, char_align, flavor_txt, hit_points, age, experience_points, character_level], character_level

def prof_bon(lvl):

    prof_dict = {1:2, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4, 12:4, 13:5, 14:5, 15:5, 16:5, 17:6, 18:6, 19:6, 20:6}
    return prof_dict[lvl]

def level_up(xp, level):

    lvl_lst = [0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000, 100000, 120000, 140000, 165000, 195000, 225000, 
    265000, 305000, 355000, 120000000]
    if lvl_lst[level] <= xp:
        return True

    return False

def attribute_incr(level):

    water_marks = [3, 7, 11, 15, 18]
    return level in water_marks

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
    password2 = request.form.get('password2')

    if password2 != password:
        flash('Passwords do not match.')
        return redirect('/register')

    if not User.query.filter_by(email=email).first():
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')

        return redirect('/')

    else:
        flash('Email already in use.')

        return redirect('/register')

@app.route('/your_characters')
def find_characters():


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')

    user_id = int(session.get('user_id'))

    all_characters = db.session.query(Character.char_id, Character.char_name, Character.user_id, 
        Character.template_id, Character.spec_id, Character.experience_points, Character.character_level, 
        Character.attributes_id).all()
    user_chars = retrieve_user_characters(all_characters, user_id)
    user_chars_expand = append_user_characters(user_chars)

    return render_template("your_characters.html", user_chars_expand=user_chars_expand)

@app.route('/upgrade_portal', methods=["POST"])
def xp_add():


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')


    attributes_id = int(request.form.get('attributes_id'))
    char_id = int(request.form.get('char_id'))
    character_level = int(request.form.get('character_level'))
    experience_points = int(request.form.get('character_level'))
    num_xp = int(request.form.get('num_xp'))
    template_id = int(request.form.get('template_id'))
    user_id = int(request.form.get('user_id'))
    user_chars_expand = request.form.getlist('user_chars_expand')


    char = char_query(char_id)
    char.experience_points += num_xp
    db.session.add(char)
    db.session.commit()
    all_characters = db.session.query(Character.char_id, Character.char_name, Character.user_id, 
        Character.template_id, Character.spec_id, Character.experience_points, Character.character_level, 
        Character.attributes_id).all()
    user_chars = retrieve_user_characters(all_characters, user_id)
    user_chars_expand = append_user_characters(user_chars)
    char = char_query(char_id)
    character_level = char.character_level
    upgrade = level_up(char.experience_points, char.character_level)
    attribute_names = ['strength', 'dexterity', 'constitution', 'wisdom', 'intelligence', 'charisma']
    if upgrade == False:
        return render_template("your_characters.html", user_chars_expand=user_chars_expand)

    else:
        char.character_level += 1
        db.session.add(char)
        db.session.commit()
        char = char_query(char_id)

        return render_template("level_up.html", attributes=retrieve_attributes(attributes_id), character_level=char.character_level, 
                                conmod=modifiers(retrieve_attributes(attributes_id)[2]), hit_points=char.hit_points, 
                                hit_dice=template_query(template_id).hit_dice, attrib_plus=attribute_incr(character_level), 
                                attribute_names=attribute_names, user_id=user_id, template_id=template_id, experience_points=char.experience_points, 
                                spec_id=char.spec_id, flavor_txt=char.flavor_txt, char_align=char.char_align, 
                                age=char.age, char_name=char.char_name, attributes_id=char.attributes_id, char_id=char_id)


@app.route('/character_start')
def start_making_character():

    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')

    temp_nfo = db.session.query(Template.template_id, Template.template_name).all()
    spec_nfo = db.session.query(Char_species.spec_id, Char_species.spec_type).all()

    return render_template("character_start.html", temp_nfo=temp_nfo, spec_nfo=spec_nfo)

@app.route('/character_start', methods=["POST"])
def first_form():

    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')

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


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')


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

    mod = modifiers(constitution)
    hit_points = hitdice + mod

    return render_template('/dependencies.html', user_id=user_id, template_id=template_id, spec_id=spec_id,
        char_name=char_name, flavor_txt=flavor_txt, age=age, strength=strength, char_align=char_align,
        dexterity=dexterity, constitution=constitution, intelligence=intelligence, hit_points=hit_points,
        wisdom=wisdom, charisma=charisma, experience_points=experience_points, character_level=character_level, 
        mod=mod, hitdice=hitdice)



@app.route('/dependencies', methods=["POST"])
def commit_char_attr():


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')


    age = int(request.form.get('age'))
    attributes_id = request.form.get('attributes_id')
    attr_inc_1 = request.form.get('attr_inc_1')
    attr_inc_2 = request.form.get('attr_inc_2')
    char_align = request.form.get('char_align')
    char_id = request.form.get('char_id')
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

    if character_level == 1:


        #creates attribute object
        attributes = Attribute(strength=strength, dexterity=dexterity, constitution=constitution, wisdom=wisdom, intelligence=intelligence, charisma=charisma)

        #adds attribute object to the session and flushes
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

    else:

        attributes_id = int(attributes_id)
        char_id = int(char_id)

        if attr_inc_1:

            add_attribute_inc(attr_inc_1, attr_inc_2, strength, dexterity, constitution, intelligence, 
                wisdom, charisma, attributes_id)


        character  = char_query(char_id)

        character.hit_points = hit_points

        db.session.add(character)
        db.session.commit()

    #retrieves character id
    char = db.session.query(Character).order_by(Character.char_id.desc()).first()
    this_template = Template.query.filter_by(template_id=template_id).first()

    #retrieves the jsons which shows the characters accumulation of spells and special abilities
    growth_item = json.loads(this_template.growth_table)
    growth_item = growth_item[f'{character_level}']


    spells = if_spells(growth_item)

    char_id = char.char_id

    if "spells_known" in growth_item:
        del growth_item["spells_known"]

    if "bonus_spell" in growth_item:
        del growth_item["bonus_spell"]

    if "Additional Spells" in growth_item:
        del growth_item["Additional Spells"]


    if this_template.spell_ability == "null" or spells == False:

        if character_level != 1:

                this_template = Template.query.filter_by(template_id=template_id).first()
                template_name = this_template.template_name
                hitdice = this_template.hit_dice
                attributes = retrieve_attributes(attributes_id)
                spec_id, character_object, character, character_level = retrieve_character(char_id)
                race = retrieve_race(spec_id)
                skills_obj = retrieve_char_skills(char_id)
                skills_obj = retrieve_skills(skills_obj)
                spells_obj = retrieve_char_spells(char_id)
                spells_obj = retrieve_spells(spells_obj)
                growth_items = json.loads(this_template.growth_table)
                growth_item = growth_items[f'{character_level}']
                feats = json.loads(this_template.features_table)
                prof = prof_bon(character[6])
                sneak = growth_item.get("sneak_attack", "POOP")
                rages = sum([item.get("rages", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
                rage_damage = sum([item.get("rage_damage", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
                barbarian = [rages, rage_damage]
                spells_known = sum([item.get("spells_known", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
                feat_list = [item for lvl, item in feats.items() if int(lvl) <= character_level and item != "null"]
                monk = growth_item.get("Ki Points", 0), growth_item.get("Unarmored Movement", 0)

                return render_template("commit_char_true.html", attributes_id=attributes_id, template_id=template_id, this_template=this_template, 
                    attributes=attributes, hitdice=hitdice, character=character, race=race, skills_obj=skills_obj, char_id=char_id, 
                    spells_obj=spells_obj, sneak=sneak, barbarian=barbarian, spells_known=spells_known, feat_list=feat_list, template_name=template_name, 
                    monk=monk, prof=prof)

        else:

            skills = []

            skill_nfo, skills_num = this_template.skill_choices, this_template.num_skills
            skill_info = skill_nfo.rsplit(', ')

            for i in skill_info:
                i = int(i)
                skill_obj = Skill.query.get(i)
                skills.append((skill_obj.skill_id, skill_obj.skill_name))

            num_skills = list(range(1, skills_num+1))
            other_list = compliment_list(num_skills, 6)

            return render_template("add_skills.html", template_id=template_id, skills=skills, num_skills=num_skills, other_list=other_list, char_id=char_id,
                user_id=user_id, attributes_id=attributes_id)
    else:


        char = char_query(char_id)
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

    return render_template("add_spells.html", growth_list=growth_list, spell_objects=spell_objects, specific_spells=specific_spells, 
        unvariety=unvariety, template_id=template_id, user_id=user_id, char_id=char_id, attributes_id=attributes_id, character_level=char.character_level) 

@app.route('/add_skills_after_spells', methods=["POST"])
def skills_after_spells():


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')


    attributes_id = int(request.form.get('attributes_id'))
    char_id = int(request.form.get('char_id'))
    character_level = int(request.form.get('character_level'))
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

    if character_level == 1:
        return render_template("add_skills_after_spells.html", template_id=template_id, user_id=user_id, 
                char_id=char_id, other_list=other_list, num_skills=num_skills, skills=skills, attributes_id=attributes_id) 

    else:
        this_template = Template.query.filter_by(template_id=template_id).first()
        template_name = this_template.template_name
        hitdice = this_template.hit_dice
        attributes = retrieve_attributes(attributes_id)
        spec_id, character_object, character, character_level = retrieve_character(char_id)
        race = retrieve_race(spec_id)
        skills_obj = retrieve_char_skills(char_id)
        skills_obj = retrieve_skills(skills_obj)
        spells_obj = retrieve_char_spells(char_id)
        spells_obj = retrieve_spells(spells_obj)
        growth_items = json.loads(this_template.growth_table)
        growth_item = growth_items[f'{character_level}']
        feats = json.loads(this_template.features_table)
        prof = prof_bon(character[6])
        sneak = growth_item.get("sneak_attack", "POOP")
        rages = sum([item.get("rages", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
        rage_damage = sum([item.get("rage_damage", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
        barbarian = [rages, rage_damage]
        spells_known = sum([item.get("spells_known", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
        feat_list = [item for lvl, item in feats.items() if int(lvl) <= character_level and item != "null"]
        monk = growth_item.get("Ki Points", 0), growth_item.get("Unarmored Movement", 0)

        return render_template("commit_char_true.html", attributes_id=attributes_id, template_id=template_id, this_template=this_template, 
            attributes=attributes, hitdice=hitdice, character=character, race=race, skills_obj=skills_obj, char_id=char_id, 
            spells_obj=spells_obj, sneak=sneak, barbarian=barbarian, spells_known=spells_known, feat_list=feat_list, template_name=template_name, 
            monk=monk, prof=prof)

@app.route('/commit_char_true', methods=["POST"])
def commit_show_char():


    try:
        assert 'user_id' in session
    except:
        AssertionError
        flash('You must be logged in')
        return redirect('/')


    attributes_id = int(request.form.get('attributes_id'))
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

    this_template = Template.query.filter_by(template_id=template_id).first()
    template_name = this_template.template_name
    hitdice = this_template.hit_dice
    attributes = retrieve_attributes(attributes_id)
    spec_id, character_object, character, character_level = retrieve_character(char_id)
    race = retrieve_race(spec_id)
    skills_obj = retrieve_char_skills(char_id)
    skills_obj = retrieve_skills(skills_obj)
    spells_obj = retrieve_char_spells(char_id)
    spells_obj = retrieve_spells(spells_obj)
    growth_items = json.loads(this_template.growth_table)
    growth_item = growth_items[f'{character_level}']
    feats = json.loads(this_template.features_table)
    prof = prof_bon(character[6])
    sneak = growth_item.get("sneak_attack", "POOP")
    rages = sum([item.get("rages", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
    rage_damage = sum([item.get("rage_damage", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
    barbarian = [rages, rage_damage]
    spells_known = sum([item.get("spells_known", 0) for lvl, item in growth_items.items() if int(lvl) <= character_level])
    feat_list = [item for lvl, item in feats.items() if int(lvl) <= character_level and item != "null"]
    monk = growth_item.get("Ki Points", 0), growth_item.get("Unarmored Movement", 0)

    return render_template("commit_char_true.html", attributes_id=attributes_id, template_id=template_id, this_template=this_template, 
        attributes=attributes, hitdice=hitdice, character=character, race=race, skills_obj=skills_obj, char_id=char_id, 
        spells_obj=spells_obj, sneak=sneak, barbarian=barbarian, spells_known=spells_known, feat_list=feat_list, template_name=template_name, 
        monk=monk, prof=prof)

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
        return redirect('/')


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

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)