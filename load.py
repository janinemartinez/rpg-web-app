import json
from sqlalchemy import func
from server import app

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


# arrow_spell.templates

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# def set_val_template_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(Template.template_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('templates_template_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()

# def set_val_spec_id():
#     """Set value for the next spec_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(Char_species.spec_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next spec_id to be max_id + 1
#     query = "SELECT setval('char_species_spec_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()

# def set_val_spell_id():
#     """Set value for the next spell_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(Spell.spell_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next spell_id to be max_id + 1
#     query = "SELECT setval('spells_spell_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()



    load_json_file("JSON/template2.json", Template,
    key_map={
        "name": "template_name",
        "temp_desc": "temp_desc",
        "hit_dice": "hit_dice",
        "prof_saving_throws": "saving_throws",
        "skills": "num_skills",
        "skill_choices": "skill_choices",
        "table": "user_table",
        "feats": "features_table",
        "growth_table": "growth_table",
        "spellcasting_ability": "spell_ability"
    })

    load_json_file("JSON/race.json", Char_species,
    key_map={
        "name": "spec_type",
        "spec_desc": "spec_desc",
        "asi": "asi",
        "age": "age_nfos",
        "alignment": "align_nfos",
        "size": "size_nfos",
        "speed_desc": "speed_nfos",
        "languages": "languages",
        "vision": "vision",
        "traits": "traits",
        "speed": "speed"
    })


    load_json_file("JSON/spells2.json", Spell,
    key_map={
        "name": "spell_name",
        "spell_desc": "spell_desc",
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

    load_json_file("JSON/skills.json", Skill,
    key_map={
        "skill_id": "skill_id",
        "skill_name": "skill_name",
        "skill_desc": "skill_desc",
        "attribute": "attribute",

    })
    # set_val_template_id()
    # set_val_spec_id()
    # set_val_spell_id()




