from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from model import ParkinsonResult
import pickle
with open('parkinsons_model.pkl', 'rb') as f:
    parkinson_model = pickle.load(f)


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.debug = True

class User(db.Model):
    __tablename__ = 'user'  # explicitly define the table name
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
with app.app_context():
   db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
            # Add authentication logic if required
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            # If the user exists, check the password
            if user.password == password:
                return redirect(url_for('home', username=username))
            else:
                error = "Invalid password"
                return render_template('login.html', error=error)
        else:
            #If the user does not exist, create a new user
            with app.app_context():
                print("Creating new user")
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('home', username=username))
    
    return render_template('login.html')
@app.route('/home', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
        # You can process the login data here if needed
        # Add authentication logic if required
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user already exists
    return render_template('home.html')

@app.route('/parkinson', methods=['GET', 'POST'])
def parkinson():
    result = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.args.get('username')  # logged-in user
        
        features = [
            float(request.form.get('MDVP:Fo(Hz)')),
            float(request.form.get('MDVP:Fhi(Hz)')),
            float(request.form.get('MDVP:Flo(Hz)')),
            float(request.form.get('MDVP:Jitter(%)')),
            float(request.form.get('MDVP:Jitter(Abs)')),
            float(request.form.get('MDVP:RAP')),
            float(request.form.get('MDVP:PPQ')),
            float(request.form.get('Jitter:DDP')),
            float(request.form.get('MDVP:Shimmer')),
            float(request.form.get('MDVP:Shimmer(dB)')),
            float(request.form.get('Shimmer:APQ3')),
            float(request.form.get('Shimmer:APQ5')),
            float(request.form.get('MDVP:APQ')),
            float(request.form.get('Shimmer:DDA')),
            float(request.form.get('NHR')),
            float(request.form.get('HNR')),
            float(request.form.get('RPDE')),
            float(request.form.get('DFA')),
            float(request.form.get('spread1')),
            float(request.form.get('spread2')),
            float(request.form.get('D2')),
            float(request.form.get('PPE'))

        ]

        prediction = parkinson_model.predict([features])[0]
        result_text = "Positive" if prediction == 1 else "Negative"

        # Save to DB
        user = User.query.filter_by(username=username).first()
        if user:
            new_result = ParkinsonResult(name=name, prediction=result_text)
            db.session.add(new_result)
            db.session.commit()

        result = f"{name} has a {result_text} result for Parkinson’s"

    return render_template('parkinson.html', result=result)

@app.route('/heart', methods=['GET', 'POST'])
def heart():
    result = None
    if request.method == 'POST':
        result = "Model not available yet. Prediction coming soon."
    return render_template('heart.html', result=result)

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    result = None
    if request.method == 'POST':
        result = "Model not available yet. Prediction coming soon."
    return render_template('diabetes.html', result=result)

if __name__ == '__main__':
    app.run()