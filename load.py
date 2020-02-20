import json
from sqlalchemy import func
# from model import Class_spell
# from model import Char_spell
# from model import Skill
# from model import Char_skill
from server import app

from model import (
    User, 
    Character,
    Template,
    Spell,
    Char_species,
    connect_to_db,
    db,
)



def load_json_file(filename, klass, key_map):

    with open(filename) as f:
        data = f.read()

    data = json.loads(data)
    results = data['results']


    for i in results:
        param_dict = {}
        for k,v in i.items():
            if k in key_map:
                if type(v) in [type(dict()), type(list())]:
                    v = json.dumps(v)
                param_dict[key_map[k]] = v
        obj = klass(**param_dict)

        db.session.add(obj)

    db.session.commit()

            

# for res in results:
#   spell = Spell(name=res['name'])
#   temp_names = res['dnd_class'].split(', ')
#   for name in temp_names:
#       template = Template.query.filter_by(template_name=name).first()
#       spell.templates.append(template)

    # commit...



# arrow_spell.templates

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_template_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Template.template_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('templates_template_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_spec_id():
    """Set value for the next spec_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Char_species.spec_id)).one()
    max_id = int(result[0])

    # Set the value for the next spec_id to be max_id + 1
    query = "SELECT setval('char_species_spec_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_spell_id():
    """Set value for the next spell_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Spell.spell_id)).one()
    max_id = int(result[0])

    # Set the value for the next spell_id to be max_id + 1
    query = "SELECT setval('spells_spell_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()



    load_json_file("JSON/template", Template,
    key_map={
        "name": "template_name",
        "desc": "desc",
        "hit_dice": "hit_dice",
        "prof_saving_throws": "saving_throws",
        "skills": "num_skills",
        "prof_skills": "skill_choices",
        "table": "user_table",
        "feats": "features_table",
        "growth_table": "growth_table",
        "spellcasting_ability": "spell_ability"
    })

    load_json_file("JSON/race", Char_species,
    key_map={
        "name": "spec_type",
        "desc": "spec_description",
        "asi": "spec_stat_mod",
        "age": "age_nfos",
        "alignment": "align_nfos",
        "size": "size_nfos",
        "speed_desc": "speed_nfos",
        "languages": "languages",
        "vision": "vision",
        "traits": "traits"
    })


    load_json_file("JSON/spells", Spell,
    key_map={
        "name": "spell_name",
        "desc": "spell_desc",
        "higher_level": "higher_level",
        "range": "spell_range",
        "components": "components",
        "material": "material",
        "ritual": "ritual",
        "duration": "duration",
        "concentration": "concentration",
        "casting_time": "casting_time",
        "level": "spell_level",
        "level_int": "int_requirement",
        "school": "school",
        "dnd_class": "dnd_class",
        "archetype": "archetype",
        "circles": "circles"
    })

    set_val_template_id()
    set_val_spec_id()
    set_val_spell_id()




