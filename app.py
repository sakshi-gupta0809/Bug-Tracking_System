from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    reported_bugs = db.relationship('Bug', backref='reporter', lazy=True, foreign_keys='Bug.user_id')
    assigned_bugs = db.relationship('Bug', backref='assignee', lazy=True, foreign_keys='Bug.assignee_id')

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    priority = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        bugs = Bug.query.order_by(Bug.updated_at.desc()).all()
        return render_template('index.html', bugs=bugs)
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/bug/new', methods=['GET', 'POST'])
@login_required
def new_bug():
    if request.method == 'POST':
        bug = Bug(
            title=request.form.get('title'),
            description=request.form.get('description'),
            priority=request.form.get('priority'),
            status='Open',
            user_id=current_user.id
        )
        db.session.add(bug)
        db.session.commit()
        flash('Bug reported successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('bug_form.html')

@app.route('/bug/<int:bug_id>')
@login_required
def view_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return render_template('bug_detail.html', bug=bug)

@app.route('/bug/<int:bug_id>/update', methods=['GET', 'POST'])
@login_required
def update_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if bug.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this bug', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        bug.title = request.form.get('title')
        bug.description = request.form.get('description')
        bug.status = request.form.get('status')
        bug.priority = request.form.get('priority')
        db.session.commit()
        flash('Bug updated successfully!', 'success')
        return redirect(url_for('view_bug', bug_id=bug.id))
    
    return render_template('bug_form.html', bug=bug)

@app.route('/bug/<int:bug_id>/delete', methods=['POST'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if bug.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this bug', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(bug)
    db.session.commit()
    flash('Bug deleted successfully!', 'success')
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Database initialized with admin user.")

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
