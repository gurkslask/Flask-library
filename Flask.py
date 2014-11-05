from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import SubmitField, RadioField
from wtforms.validators import InputRequired, ValidationError
from flask.ext.script import Manager
import os
from LibraryFunctions import ReadProjectDict, CheckOut, CheckIn


app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = 'nidnsöf&%dsad&%7(/(212>><'
bootstrap = Bootstrap(app)


class ProjectsForm(Form):
    """docstring for ProjectsForm"""
    #Make the radiofield
    ChooseProject = RadioField('Projects',
                               validators=[InputRequired(), ]
                               )

    #SubmitField
    CheckOutSubmit = SubmitField('Check out')
    CheckInSubmit = SubmitField('Check in')


def validate_CheckOut(form, field):
    if ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked out')


def validate_CheckIn(form, field):
    if not ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked in')


@app.route('/', methods=['GET', 'POST'])
def index():
    ProjectsFormF = ProjectsForm()
    """Big mothafucka list concentation
    for populating the radio buttons in the form
    """
    ProjectsFormF.ChooseProject.choices = [(
        j, 'Project: {0}, Checked out: {1}, <a href="/info/{0}"> link </a>'.format(
            j, ReadProjectDict(j)['CheckedOut']))
        for j in os.listdir('Projects')]

    if ProjectsFormF.validate_on_submit():
        #If any submit buttons are clicked
            if ProjectsFormF.CheckInSubmit.data:
                #Check which submit button was clicked
                validate_CheckIn(ProjectsFormF, ProjectsFormF.ChooseProject)
                CheckIn(ProjectsFormF.ChooseProject.data)
            elif ProjectsFormF.CheckOutSubmit.data:
                #Check which submit button was clicked
                validate_CheckOut(ProjectsFormF, ProjectsFormF.ChooseProject)
                CheckOut(ProjectsFormF.ChooseProject.data)
    return render_template(
        'index.html',
        ProjectsFormF=ProjectsFormF
    )


@app.route('/info/<project>')
def ProjectInfo(project):
    return render_template(
        'info.html',
        project=ReadProjectDict(project)
        )


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=False)
