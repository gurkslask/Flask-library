from flask import Flask, make_response, render_template
import pickle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.script import Manager


app = Flask(__name__)
manager = Manager(app)


@app.route('/<name>')
def index(name):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=False)
