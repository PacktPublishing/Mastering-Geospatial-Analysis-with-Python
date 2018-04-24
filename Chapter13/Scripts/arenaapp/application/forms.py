from flask_wtf import FlaskForm
from wtforms import TextField, FloatField
class AddForm(FlaskForm):
	name = TextField('Arena Name')
	longitude = FloatField('Longitude')
	latitude = FloatField('Latitude')




