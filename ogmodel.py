

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """user info"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):

        return f"""<User user_id={self.user_id} email={self.email}>"""

class Character(db.Model):
    """completed characters"""

    __tablename__ = "characters"

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.template_id'), nullable=False)
    spec_id = db.Column(db.Integer, db.ForeignKey('char_species.spec_id'), nullable=False)
    char_name = db.Column(db.String(20), nullable=False)
    flavor_txt = db.Column(db.Text, nullable=True)
    hit_points= db.Column(db.Integer, nullable=False)
    age= db.Column(db.Integer, nullable=False)
    experience_points = db.Column(db.Integer, nullable=True)
    character_level = db.Column(db.Integer, nullable=False)
    num_skills = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=db.backref("characters", order_by=char_id))
    template = db.relationship("Template", backref=db.backref("characters", order_by=char_id))
    char_species = db.relationship("Char_species", backref=db.backref("characters", order_by=char_id))

    def __repr__(self):
            """Return a human-readable representation of a Human."""
            return f"""<Character char_id={self.char_id}
                        user_id={self.user_id}
                        template_id={self.template_id}
                        spec_id={self.spec_id}
                        char_name={self.char_name}
                        hit_points={self.hit_points}
                        experience_points={self.experience_points}
                        character_level={self.character_level}
                        num_skills={self.num_skills}>"""



class Template(db.Model):
    """character classes"""

    __tablename__ = "templates"

    template_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    template_name = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    hit_dice= db.Column(db.Integer, nullable=False)
    saving_throws= db.Column(db.Text, nullable=False)
    num_skills = db.Column(db.Integer, nullable=False)
    skill_choices = db.Column(db.Text, nullable=False) 
    user_table = db.Column(db.Text, nullable=False)
    features_table = db.Column(db.Text, nullable=False)
    growth_table = db.Column(db.Text, nullable=False)
    spell_ability = db.Column(db.Text, nullable=False)

    # spells = db.relationship('Spell', backref='templates', secondary='class_spells')



# class Class_spell(db.Model):
#     """spells and the classes that can weild them"""

#     __tablename__ = "class_spells"

#     class_spell_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     spell_id = db.Column(db.Integer, db.ForeignKey('spell_list.spell_id'), nullable=False)
#     template_id = db.Column(db.Integer, db.ForeignKey('template.template_id'), nullable=False)
#     template_type = db.Column(db.String(20), db.ForeignKey('template.template_type'), nullable=False)

#     spell_id = db.relationship("Spell", backref=db.backref("class_spells", order_by=class_spell_id))
#     template_id = db.relationship("Template", backref=db.backref("class_spells", order_by=class_spell_id))
#     template_type = db.relationship("Template", backref=db.backref("class_spells", order_by=class_spell_id))   

class Spell(db.Model):

    __tablename__= "spells"

    spell_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spell_name = db.Column(db.Text, nullable=False)
    spell_desc = db.Column(db.Text, nullable=False)
    higher_level = db.Column(db.Text, nullable=False)
    spell_range = db.Column(db.Text, nullable=False)
    components = db.Column(db.Text, nullable=False)
    material = db.Column(db.Text, nullable=False)
    ritual = db.Column(db.Text, default=False, nullable=False)
    duration = db.Column(db.Text, nullable=False)
    concentration = db.Column(db.Text, default=False, nullable=False)
    casting_time = db.Column(db.Text, nullable=False)
    spell_level = db.Column(db.Text, nullable=False)
    int_requirement = db.Column(db.Integer, nullable=False)
    school = db.Column(db.Text, nullable=False)
    dnd_class = db.Column(db.Text, nullable=False)
    archetype = db.Column(db.Text, nullable=True)
    circles = db.Column(db.Text, nullable=True)

# class Char_spell(db.Model):

#     __tablename__="char_spells"

#     c_spell_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     spell_id = db.Column(db.Integer, db.ForeignKey('spell_list.spell_id'), nullable=False)
#     char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'), nullable=False)

#     spell_id = db.relationship("Spell", backref=db.backref("char_spells", order_by=c_spell_id))
#     charl_id = db.relationship("Character", backref=db.backref("char_spells", order_by=c_spell_id))


# class Class_skill(db.Model):
#     """spells and the classes that can weild them"""

#     __tablename__ = "class_skills"

#     class_skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     skill_id = db.Column(db.Integer, db.ForeignKey('skill_list.skill_id'), nullable=False)
#     template_id = db.Column(db.Integer, db.ForeignKey('template.template_id'), nullable=False)

#     skill_id = db.relationship("Skill_list", backref=db.backref("class_skills", order_by=class_skill_id))
#     template_id = db.relationship("Template", backref=db.backref("class_skills", order_by=class_skill_id))

class Skill(db.Model):

    __tablename__= "skills"

    skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    skill_name = db.Column(db.String(20), nullable=False)
    skill_desc = db.Column(db.String(60), nullable=False)

# class Char_skill(db.Model):

#     __tablename__="char_skills"

#     c_skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), nullable=False)
#     char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'), nullable=False)

#     skill_id = db.relationship("Skill", backref=db.backref("char_skills", order_by=c_skill_id))
#     charl_id = db.relationship("Character", backref=db.backref("char_skills", order_by=c_skill_id))

class Char_species(db.Model):

    __tablename__= "char_species"

    spec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spec_type = db.Column(db.String(20), nullable=False)
    #species bonus, traits, age, align, size, speed, speed desc, languages, vision
    spec_description = db.Column(db.String(3000), nullable=False)
    age_nfos = db.Column(db.Text, nullable=False)
    align_nfos = db.Column(db.Text, nullable=False)
    size_nfos = db.Column(db.Text, nullable=False)
    speed_nfos = db.Column(db.Text, nullable=False)
    languages = db.Column(db.Text, nullable=False)
    vision = db.Column(db.Text, nullable=False)
    traits = db.Column(db.Text, nullable=False)
    #asi
    spec_stat_mod = db.Column(db.Text, nullable=False)

    def __repr__(self):
            """Return a human-readable representation of a Human."""
            return f"""<Char_species spec_id={self.spec_id}
                        spec_type={self.spec_type}
                        age_nfos={self.size_nfos}
                        align_nfos={self.align_nfos}
                        size_nfos={self.size_nfos}
                        languages={self.languages}
                        vision={self.vision}
                        spec_stat_mod={self.spec_stat_mod}>"""


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///role_playing'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

