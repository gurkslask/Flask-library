from flask import render_template, redirect, url_for, session, request
from . import main
from .forms import (ProjectsForm, InitForm, dlRdy, UploadZip)
from .LibraryFunctions import Libraryfunctions
from wtforms.validators import ValidationError
from flask.ext import uploads
import os
from werkzeug import secure_filename, FileStorage


Lf = Libraryfunctions()
ZipUpload = uploads.UploadSet('zipfiles')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads/')
ALLOWED_EXTENSIONS = set(['zip'])


@main.route('/', methods=['GET', 'POST'])
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
        #If there is no projects
        return render_template('empty.html', text='No projects')
    if ProjectsFormF.validate_on_submit():
        session['Project'] = ProjectsFormF.ChooseProject.data
        #If any submit buttons are clicked
        if ProjectsFormF.CheckInSubmit.data:
            #Check which submit button was clicked
            validate_CheckIn(ProjectsFormF, ProjectsFormF.ChooseProject)
            print('Checka in {}'.format(session['Project']))
            Lf.CheckIn(session['Project'])
            return redirect(url_for('main.index'))
        elif ProjectsFormF.CheckOutSubmit.data:
            #Check which submit button was clicked
            validate_CheckOut(ProjectsFormF, ProjectsFormF.ChooseProject)
            Lf.ZipProject(session['Project'])
            #Send to download page
            download()
            return redirect(url_for('main.download'))
    return render_template('projects.html',
                           ProjectsFormF=ProjectsFormF,
                           projects=session['Project']
                           )


@main.route('/download', methods=['GET', 'POST'])
def download():
    dlRdyF = dlRdy()
    if dlRdyF.validate_on_submit():
        if dlRdyF.dlRdySubmit.data:
            #When the download is ready and the project is ready for checkout
            Lf.CheckOut(session['Project'])
            Lf.DeleteProject(session['Project'] + '.zip')
            session['Project'] = None
            return redirect(url_for('main.index'))
    return render_template(
        'dlProject.html', project=session['Project'], dlRdyF=dlRdyF)


def validate_filename(filename):
    if '.' not in filename and filename.rsplit('.', 1)[1] not in ALLOWED_EXTENSIONS:
        raise ValidationError('Not a zip file')


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            validate_filename(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return 'Uploaded!'
    return render_template(
        'ulProject_html.html'
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
