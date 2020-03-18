# The Periwinkle Kobold

The Periwinkle Kobold is a full-stack web application meant to save time and labor for those creating assets for Dungeons and Dragons 5E role playing game. The feature I've currently implemented are the Registration, Login, Character Generator, the interface for recalling characters you've already created, and an avenue for upgrading those characters once you've accumulated experience points through adventuring. Initially the user picks between basic options. Which Class, Race, Alignment, and what Name are amongst the first options once you decide to build a character. Once these choices are made a table will be seeded with dice. Your initial choices will contribute to your end values as your ability scores are generated through java-script dice. Once you've finished determining ability cores, hit points, spells, skills, and such the application will generate a printable character sheet for use in the game. After a game session you can load the new experience points and they will either be recorded in your database, or they will trigger database queries that will begin an increase in level, and enable to user to initiate all the subsequent improvements.

# Overview
### User Interface

- Sign up for an account
- Log in
- Initiate the creation of the character
- Upgrade said character
- Access any of your Characters

### Character creation

- Choose from a list of initial options
- Choose from options initiated by the initial choices
- Character features that rely on the Characters current level, class, and race but aren't chosen are attributed to the character automatically
- The character is able to be printed in it's form for use with your next game.

# Technical Stack

### Front

- Java Script, JQuery, Jinja, HTML5, CSS, Bootstrap

### Back

- Postgres SQL, SQL Alchemy, Flask, Python

### API

Django Rest Framework

