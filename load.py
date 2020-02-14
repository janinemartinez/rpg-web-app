import json
import requests
# from sqlalchemy import func
# from model import User
# from model import Character
# from model import Template
# from model import Class_spell
# from model import Spell
# from model import Char_spell
# from model import Skill
# from model import Char_skill
# from model import Char_species
# from model import connect_to_db, db
# from server import app




def load_templates():

	with open('JSON/Class') as f:
		data = f.read()

	data = json.loads(data)
	results = data['results']
	# tbl = results[0]['table']

	for i in results:
		dict_list = []
		for l in i:
			dict_list.append(i[l])
			print(dict_list)


load_templates()
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
	














# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# if __name__ == "__main__":
#     connect_to_db(app)

#     # In case tables haven't been created, create them
#     db.create_all()

#     # Import different types of data
#     load_users()
#     load_characterss()
#     load_templates()
#     load_class_spells()
#     load_spells()
#     load_char_spells()
#     load_skills()
#     load_char_skills()
#     load_char_species()
#     set_val_user_id()






