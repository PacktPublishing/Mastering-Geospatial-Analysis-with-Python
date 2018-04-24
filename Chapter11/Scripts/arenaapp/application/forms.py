from flask_wtf import FlaskForm
from wtforms import SelectField
class ArenaForm(FlaskForm):
	description  = "Use the dropdown to select an arena."
	selections = SelectField('Select an Arena',choices=[])




