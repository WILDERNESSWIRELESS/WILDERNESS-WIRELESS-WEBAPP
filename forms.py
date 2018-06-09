from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Enter')

class BatLoForm(FlaskForm):
    batloval = IntegerField('BAT_LO', validators=[DataRequired()])
    submit = SubmitField('SET')

class BatHiForm(FlaskForm):
    bathival = IntegerField('BAT_HI', validators=[DataRequired()])
    submit = SubmitField('SET')

class CmdForm(FlaskForm):
    cmdval = StringField('CMD', validators=[DataRequired()])
    submit = SubmitField('SEND')



