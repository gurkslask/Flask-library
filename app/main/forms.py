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


def validate_CheckOut(form, field):
    if Lf.ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked out')


def validate_CheckIn(form, field):
    if not Lf.ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked in')


class InitForm(Form):
    """docstring for initform"""
    InitProjectName = TextField('Name of project',
                                validators=[InputRequired()]
                                )
    submit = SubmitField('Initiate!')
