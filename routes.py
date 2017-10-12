from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Length
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['SECRET_KEY'] = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:password@localhost/noteapp'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'noteapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
mysql.init_app(app)
db = SQLAlchemy(app)

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(120))
	date = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Note {}, Time {}>'.format(self.text, self.date)


class Note_Form(Form):
	add_note_button = SubmitField('add note')
	delete_button = SubmitField('delete')
	field = TextAreaField('input', validators=[InputRequired(), Length(min=1,max=50)])

	
@app.route('/',methods=['GET', 'POST'])
def index():
	text = None
	note_form = Note_Form()
	notes = Note.query.all()
	selected_note = None
	if request.method == 'POST' and note_form.validate():
		if note_form.add_note_button.data:
			text = note_form.field.data
			db.session.add(Note(text=text))
			db.session.commit()
			return redirect(url_for('index'))
		
	return render_template('index.html', note_form=note_form, notes=notes)

@app.route('/delete/<string:id>', methods=['GET','POST'])
def delete(id):
	note_form = Note_Form()
	selected_note = None
	if request.method == 'POST':
		selected_note = Note.query.get(id)
		db.session.delete(selected_note)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', note_form=note_form, id=id)

if __name__ == '__main__':
  app.run(debug=True)