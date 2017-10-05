from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)

app.config['SECRET_KEY'] = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)   


class Note(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(120))
	date = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Note {}, Time {}>'.format(self.text, self.date)


class Note_Form(Form):
	add_note_button = SubmitField('add note')
	edit_button = SubmitField('edit')
	save_button = SubmitField('save')
	delete_button = SubmitField('delete')
	field = TextAreaField('input', validators=[InputRequired(), Length(min=1,max=50)])

	
@app.route('/',methods=['GET', 'POST'] )
def index():
	text = None
	note_form = Note_Form()
	notes = Note.query.all()
	
	if note_form.validate_on_submit():
		if note_form.add_note_button.data:
			text = note_form.field.data
			db.session.add(Note(text=text))
			db.session.commit()
			return redirect(url_for('index'))
		
	return render_template('index.html', note_form=note_form, notes=notes)

		
			



 
if __name__ == '__main__':
  app.run(debug=True)