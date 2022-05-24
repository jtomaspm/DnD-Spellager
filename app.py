from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from functions import *
import json



#initial setup
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'verysecretkeymuchwow123'



#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#Database classes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    json = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Spell %r>' % self.index

class Assoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    index = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Assoc %r>' % self.username



#Form templates
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"paceholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"paceholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        db_usernames = User.query.filter_by(
            username=username.data
        ).first()
        if db_usernames:
            raise ValidationError("Username already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"paceholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"paceholder": "Password"})
    submit = SubmitField("Login")



#Home
@app.route('/')
@login_required
def index():
    return render_template('home.html')


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('register.html', form=form)


#Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#Spells
@app.route('/spells', methods=['GET', 'POST'])
@login_required
def spells():
    search_query = request.args.get('search_query')
    spell_not_found = False
    no_assoc = True
    spell_json = None
    if search_query:
        index = name_to_id(search_query)
        #check database
        spell = Spell.query.filter_by(index=index).first()
        if spell:
            spell_json=json.loads(spell.json)
        else:
            #check 5e api
            spell_json = get_json_from_api(index)
            if spell_json:
                spell_json_str = json.dumps(spell_json)
                new_spell = Spell(index=index, name=spell_json['name'], json=spell_json_str)
                db.session.add(new_spell)
                db.session.commit()
            #spell not found, add spell?
            else:
                spell_not_found = True
        #Check for assoc
        if not spell_not_found:
            assoc = Assoc.query.filter_by(username=current_user.username, index=index).first()
            if assoc:
                no_assoc = False
    return render_template('spells.html', search_query=search_query, spell_not_found=spell_not_found, spell_json=spell_json, no_assoc=no_assoc)


#Add Single Spell
@app.route('/addspelltochar', methods=['GET', 'POST'])
@login_required
def addspelltochar():
    index = request.args.get('spell_index')
    if index:
        spell = Spell.query.filter_by(index=index).first()
        if spell:
            #add assoc
            new_assoc = Assoc(username=current_user.username, index=index)
            db.session.add(new_assoc)
            db.session.commit()
    return redirect(url_for('spells'))


#Beasts
@app.route('/beasts')
@login_required
def beasts():
    return render_template('beasts.html')


#Quick build
@app.route('/quick')
@login_required
def quick():
    return render_template('quick.html')


#User profile
@app.route('/user')
@login_required
def user():
    spells = []
    assocs = Assoc.query.filter_by(username=current_user.username).all()
    order_by = request.args.get('order_by')
    last_filter = request.args.get('last_filter')
    if assocs:
        for assoc in assocs:
            spells.append(json.loads(Spell.query.filter_by(index=assoc.index).first().json))
    print(spells)
    return render_template('user.html', username=current_user.username, spells=spells, order_by=order_by, last_filter=last_filter)


#Delete spell from user's table
@app.route('/delete')
@login_required
def delete():
    index = request.args.get('spell_index')
    if index:
        a = Assoc.query.filter_by(username=current_user.username, index=index).first()
        db.session.delete(a)
        db.session.commit()

    return redirect(url_for('user'))


#Add multiple spells to user's table
@app.route('/addmultiple', methods=['GET', 'POST'])
@login_required
def addmultiple():
    if request.method == 'POST':
        spell_names = request.form.get('spells').split('\r\n')
        spell_query = query_for_spells(Spell, db, spell_names, current_user.username, Assoc)
        r = '?not_found='
        for s in spell_query['not_found']:
            r += (s+'\r\n')

        return redirect(url_for('addmanualspell')+r)
    return 'addmultiple'


#Add manual spell to user's table
@app.route('/addmanualspell', methods=['GET', 'POST'])
@login_required
def addmanualspell():
    not_found = request.args.get('not_found')
    if not_found:
        not_found = not_found.split('\r\n')
        not_found = [id_to_name(id) for id in not_found]

    #handle add new spell
    if request.method == 'POST':
        form = request.form
        print(form)
        new_manual_spell(Spell, Assoc, db, form, current_user.username)
    return render_template('addmanualspell.html', not_found=not_found)


#Start Flask App
if __name__ == "__main__":
    app.run(debug=True)