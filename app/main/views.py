from flask import render_template, redirect, url_for, session
from . import main
from .forms import (ProjectsForm, InitForm, dlRdy)
from .LibraryFunctions import Libraryfunctions
import os


Lf = Libraryfunctions()


@main.route('/', methods=['GET', 'POST'])
def index():
    ProjectsFormF = ProjectsForm()
    dlRdyF = dlRdy()
    """Big mothafucka list concentation
    for populating the radio buttons in the form
    """
    ProjectsFormF.ChooseProject.choices = [(
        j, 'Project: {0}, Checked out: {1}, <a href="/info/{0}"> link </a>'.format(
            j, Lf.ReadProjectDict(j)['CheckedOut']))
        for j in os.listdir(Lf.ProjectFolderPath)]

    if len(ProjectsFormF.ChooseProject.choices) == 0:
        #If there is no projects
        return render_template('empty.html', text='No projects')
    if ProjectsFormF.validate_on_submit():
        #If any submit buttons are clicked
        session['Project'] = session['Project']
        if ProjectsFormF.CheckInSubmit.data:
            #Check which submit button was clicked
            validate_CheckIn(ProjectsFormF, ProjectsFormF.ChooseProject)
            Lf.ZipProject(session['Project'])
            Lf.CheckIn(session['Project'])
        elif ProjectsFormF.CheckOutSubmit.data:
            #Check which submit button was clicked
            validate_CheckOut(ProjectsFormF, ProjectsFormF.ChooseProject)
            Lf.ZipProject(session['Project'])
            print(session['Project'])
            return render_template(
                'dlProject.html',
                project=session['Project'],
                dlRdyF=dlRdyF
                )
    if dlRdyF.validate_on_submit():
        Lf.CheckOut(session['Project'])
        return redirect(url_for('main.index'))
    return render_template(
        'projects.html',
        ProjectsFormF=ProjectsFormF
    )


@main.route('/test')
def test():
    return 'Test'


@main.route('/info/<project>')
def ProjectInfo(project):
    return render_template(
        'info.html',
        project=Lf.ReadProjectDict(project)
        )


@main.route('/init', methods=['GET', 'POST'])
def init():
    InitFormF = InitForm()
    if InitFormF.validate_on_submit():
        #If Initate button is pressed
        try:
            #Check if project exists
            if Lf.ReadProjectDict(InitFormF.InitProjectName.data)['CheckedOut'] is not None:
                #If it exists
                return render_template(
                    'empty.html',
                    text='Cannot create project, it already exists!')
        except Exception:
            Lf.InitProject(InitFormF.InitProjectName.data)
            return redirect(url_for('index'))

    return render_template(
        'init.html',
        InitFormF=InitFormF
        )

def validate_CheckOut(form, field):
    if Lf.ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked out')


def validate_CheckIn(form, field):
    if not Lf.ReadProjectDict(field.data)['CheckedOut']:
        raise ValidationError('Already checked in')

