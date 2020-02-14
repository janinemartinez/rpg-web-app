import json
from sqlalchemy import func
# from model import User
# from model import Character
from model import Template
# from model import Class_spell
# from model import Spell
# from model import Char_spell
# from model import Skill
# from model import Char_skill
# from model import Char_species
from model import connect_to_db, db
from server import app




def load_json_file(filename, klass, key_map):

	with open(filename) as f:
		data = f.read()

	data = json.loads(data)
	results = data['results']


	for i in results:
		param_dict = {}
		for k,v in i.items():
			if k in key_map:
			 	param_dict[key_map[k]] = v
		obj = klass(**param_dict)

		db.session.add(obj)

	db.session.commit()



			

# for res in results:
# 	spell = Spell(name=res['name'])
# 	temp_names = res['dnd_class'].split(', ')
# 	for name in temp_names:
# 		template = Template.query.filter_by(template_name=name).first()
# 		spell.templates.append(template)

	# commit...



# arrow_spell.templates






# def load_spells():

# 	res = requests.get('https://api.open5e.com/spells/')
	














def set_val_template_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Template.template_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('templates_template_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    # load_characterss()
    # load_templates()
    # load_class_spells()
    # load_spells()
    # load_char_spells()
    # load_skills()
    # load_char_skills()
    # load_char_species()

    load_json_file("JSON/Class", Template,
	key_map={
		"name": "template_name",
		"slug": "template_type",
		"desc": "desc",
		"hit_dice": "hit_dice",
		"table": "growth_table"
	})

    set_val_template_id()






