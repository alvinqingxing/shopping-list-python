from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.db'
db = SQLAlchemy(app)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(200), nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Item %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])

def index():
	if request.method == 'POST':
		item_name = request.form['item']
		new_item = Item(name = item_name)
		try:
			db.session.add(new_item)
			db.session.commit()
			return redirect('/')
		except:
			return "Your item could not be added"
	else:
		items = Item.query.order_by(Item.date_created).all()
		return render_template('index.html', items = items)

@app.route('/delete/<int:id>')
def delete(id):
	item_to_delete = Item.query.get_or_404(id)
	try:
		db.session.delete(item_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return "Your item could not be removed from the list"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
	item_to_update = Item.query.get_or_404(id)
	if request.method == 'POST':
		item_to_update.name = request.form['item']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "The item could not be updated"
	else:
		return render_template('update.html', item = item_to_update)

if __name__ == "__main__":
	app.run(debug = True)