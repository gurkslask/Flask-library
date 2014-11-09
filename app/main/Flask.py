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






if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=False)
