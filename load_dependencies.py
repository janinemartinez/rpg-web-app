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
    Class_spell,
    connect_to_db,
    db,
)


def load_spell_class():

5

    for spell in Spell.query.all():
        for name in spell.dnd_class.split(', '):
            try:
                template = Template.query.filter_by(template_name=name).first()
                class_spell = Class_spell(template_id=template.template_id, spell_id=spell.spell_id)

                db.session.add(class_spell)
            except AttributeError:
                print(f"Warning: {spell.spell_name} is trying to associate with a non-existent template {name}")
    db.session.commit()







if __name__ == "__main__":
    connect_to_db(app)

    load_spell_class()







