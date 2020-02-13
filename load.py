import json
import requests
from sqlalchemy import func
from model import User
from model import Character
from model import Template
from model import Class_spell
from model import Spell
from model import Char_spell
from model import Skill
from model import Char_skill
from model import Char_species
from model import connect_to_db, db
from server import app




def load_templates():


def load_spells():






















def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_characterss()
    load_templates()
    load_class_spells()
    load_spells()
    load_char_spells()
    load_skills()
    load_char_skills()
    load_char_species()
    set_val_user_id()






