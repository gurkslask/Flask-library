from flask import Flask, render_template, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import SubmitField, RadioField, TextField
from wtforms.validators import InputRequired, ValidationError
from flask.ext.script import Manager
import os
from LibraryFunctions import Libraryfunctions


app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = 'nidnsöf&%dsad&%7(/(212>><'
bootstrap = Bootstrap(app)
Lf = Libraryfunctions()


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


@app.route('/', methods=['GET', 'POST'])
def index():
    ProjectsFormF = ProjectsForm()
    """Big mothafucka list concentation
    for populating the radio buttons in the form
    """
    ProjectsFormF.ChooseProject.choices = [(
        j, 'Project: {0}, Checked out: {1}, <a href="/info/{0}"> link </a>'.format(
            j, Lf.ReadProjectDict(j)['CheckedOut']))
        for j in os.listdir(Lf.ProjectFolderPath)]
    if len(ProjectsFormF.ChooseProject.choices) == 0:
        return render_template('empty.html', text='No projects')
    if ProjectsFormF.validate_on_submit():
        #If any submit buttons are clicked
            if ProjectsFormF.CheckInSubmit.data:
                #Check which submit button was clicked
                validate_CheckIn(ProjectsFormF, ProjectsFormF.ChooseProject)
                Lf.ZipProject(ProjectsFormF.ChooseProject.data)
                Lf.CheckIn(ProjectsFormF.ChooseProject.data)
            elif ProjectsFormF.CheckOutSubmit.data:
                #Check which submit button was clicked
                validate_CheckOut(ProjectsFormF, ProjectsFormF.ChooseProject)
                Lf.CheckOut(ProjectsFormF.ChooseProject.data)
    return render_template(
        'projects.html',
        ProjectsFormF=ProjectsFormF
    )


@app.route('/info/<project>')
def ProjectInfo(project):
    return render_template(
        'info.html',
        project=Lf.ReadProjectDict(project)
        )


class InitForm(Form):
    """docstring for initform"""
    InitProjectName = TextField('Name of project',
                                validators=[InputRequired()]
                                )
    submit = SubmitField('Initiate!')


@app.route('/init', methods=['GET', 'POST'])
def init():
    InitFormF = InitForm()
    if InitFormF.validate_on_submit():
        #If Initate button is pressed
        try:
            #Check if project exists
            if Lf.ReadProjectDict(InitFormF.InitProjectName.data)['CheckedOut'] is not None:
                #If it exists, present the user to a Confirm form
                return render_template(
                    'empty.html',
                    text = 'Cannot create project, it already exists!')
        except Exception:
            Lf.InitProject(InitFormF.InitProjectName.data)
            return redirect(url_for('index'))

    return render_template(
        'init.html',
        InitFormF=InitFormF
        )

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=False)
