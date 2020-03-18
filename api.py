from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.sqlite


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empower.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.first_name


@app.route('/api/login', methods=['POST'])
def login():
    user_id = request.form['user_id']

    exists = User.query.filter_by(id=user_id).all() != []

    return jsonify({'login': str(exists)})


@app.route('/api/signup', methods=['POST'])
def signup():
    fname = request.form['first_name']
    lname = request.form['last_name']

    if not fname.strip() or not lname.strip():
        abort(400)

    user = User(first_name=fname, last_name=lname)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User inserted into database.'})


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': str(e)}), 400
