from model import db, User, Character, Template, Spell, Char_species



# def asi_fetch(spec_id):

# 	asi_all_spec = Char_species.query.filter(Char_species.spec_stat_mod).all()
# 	asi_spec = asi_all_spec(spec_id = spec_id)
# 	print(asi_spec)



# asi_fetch(4)



if __name__ == "__main__":
    from server import app
    from model import connect_to_db

    connect_to_db(app)