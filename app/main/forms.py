from wtforms import SubmitField, RadioField, TextField
from wtforms.validators import InputRequired, ValidationError
from flask.ext.wtf import Form


class ProjectsForm(Form):
    """docstring for ProjectsForm"""
    #Make the radiofield
    ChooseProject = RadioField('Projects',
                               validators=[InputRequired(), ]
                               )

    #SubmitField
    CheckOutSubmit = SubmitField('Check out')
    CheckInSubmit = SubmitField('Check in')


class ConfirmForm(Form):
    """docstring for ConfirmForm"""
    ConfirmSubmit = SubmitField('Yes!')
    DeclineSubmit = SubmitField('No')


class InitForm(Form):
    """docstring for initform"""
    InitProjectName = TextField('Name of project',
                                validators=[InputRequired()]
                                )
    submit = SubmitField('Initiate!')


class dlRdy(Form):
    """docstring for dlRdy"""
    dlRdySubmit = SubmitField("""I've downloaded the project
    and can check the project out"""
                              )
