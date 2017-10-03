from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime 
import json
import random
from flask_sqlalchemy import SQLAlchemy

 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)   


class Note(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(120))
	date = db.Column(db.DateTime, default=datetime.utcnow)
	

	def __repr__(self):
		return '<Note {}, Time {}>'.format(self.text, self.date)

	
@app.route('/',methods=['GET', 'POST'] )
def index():
	text = None
	notes = Note.query.all()
	if request.method == 'POST' and request.form["submit"] == "add" :
		text = request.form["input"]
		db.session.add(Note(text=text))
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', notes=notes)

		
			



 
if __name__ == '__main__':
  app.run(debug=True)