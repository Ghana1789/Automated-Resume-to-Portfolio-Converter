from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os
import datetime
import re
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from ai_service import AIEnhancementService

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Set email credentials directly
app.config['MAIL_USERNAME'] = 'ghanasyamk79@gmail.com'
app.config['MAIL_PASSWORD'] = 'Gupta@1789'
app.config['MAIL_DEFAULT_SENDER'] = ('ghanasyamk79@gmail.com', 'ghanasyamk79@gmail.com')  # Set as tuple (name, address) for proper sender format

# Initialize extensions
mail = Mail(app)
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI enhancement service
ai_service = None

def init_ai_service():
    global ai_service
    if ai_service is None:
        ai_service = AIEnhancementService()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    portfolio = db.relationship('Portfolio', backref='user', uselist=False)

    def get_reset_token(self):
        return ts.dumps(self.email, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        try:
            email = ts.loads(token, salt='password-reset-salt', max_age=max_age)
            return User.query.filter_by(email=email).first()
        except:
            return None

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    summary = db.Column(db.Text)
    contact_info = db.Column(db.Text)  # Stored as JSON
    skills = db.Column(db.Text)  # Stored as JSON
    theme = db.Column(db.String(50), default='professional')
    experiences = db.relationship('Experience', backref='portfolio')

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    description = db.Column(db.Text)
    ai_enhanced_description = db.Column(db.Text)
    created_at = db.Column(db.String(100), default=lambda: datetime.datetime.now().isoformat())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    init_ai_service()
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email)
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

def parse_resume(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    content = ''
    
    if file_ext == '.pdf':
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += page.extract_text()
    elif file_ext == '.docx':
        doc = Document(file_path)
        for para in doc.paragraphs:
            content += para.text + '\n'
    
    return content

def enhance_description(text):
    # Generate an enhanced, professional description using the AI service
    return ai_service.enhance_description(text)

@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    if 'resume' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('dashboard'))
        
    file = request.files['resume']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('dashboard'))
        
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse resume content
        content = parse_resume(file_path)
        
        # Create or update portfolio
        portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
        if not portfolio:
            portfolio = Portfolio(user_id=current_user.id)
            db.session.add(portfolio)
        
        # Extract name and title from the resume if not already set
        if not portfolio.name or not portfolio.title:
            # Simple extraction of name and title from the beginning of the resume
            lines = content.split('\n')
            if len(lines) > 1:
                portfolio.name = lines[0].strip()
                if len(lines) > 2:
                    portfolio.title = lines[1].strip()
        
        # Extract contact information
        contact_info = ai_service.extract_contact_info(content)
        if contact_info:
            # Store contact info in the portfolio summary field as JSON
            import json
            portfolio.contact_info = json.dumps(contact_info)
        
        # Extract skills from resume
        skills = ai_service.extract_skills(content)
        
        # Clear existing skills (if we implement skill tables later)
        # For now, we'll store them in the summary field
        if skills:
            # Group skills by category
            skill_categories = {}
            for skill in skills:
                category = skill['category']
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill)
            
            # Store skills in portfolio summary
            portfolio.skills = json.dumps(skill_categories)
        
        # Extract and enhance experience descriptions
        experiences = content.split('\n\n')
        for exp in experiences:
            if len(exp.strip()) > 50:  # Simple check to filter out noise
                enhanced_desc = enhance_description(exp)
                
                # Try to extract company and position from the experience text
                company = ''
                position = ''
                duration = ''
                
                # Look for common patterns in resume experience sections
                lines = exp.split('\n')
                if len(lines) >= 2:
                    # First line often contains company name
                    company = lines[0].strip()
                    # Second line often contains position and duration
                    position_line = lines[1].strip()
                    
                    # Try to separate position and duration
                    if '|' in position_line:
                        parts = position_line.split('|')
                        position = parts[0].strip()
                        if len(parts) > 1:
                            duration = parts[1].strip()
                    elif '-' in position_line:
                        parts = position_line.split('-')
                        position = parts[0].strip()
                        if len(parts) > 1:
                            duration = parts[1].strip()
                    else:
                        position = position_line
                
                # Create a new experience entry
                experience = Experience(
                    portfolio=portfolio,
                    company=company,
                    position=position,
                    duration=duration,
                    description=exp,
                    ai_enhanced_description=enhanced_desc
                )
                db.session.add(experience)
        
        db.session.commit()
        os.remove(file_path)  # Clean up uploaded file
        flash('Resume processed successfully! Your professional portfolio has been created with enhanced content.')
        
        return redirect(url_for('portfolio'))

@app.route('/portfolio')
@login_required
def portfolio():
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    
    # Sort experiences by creation date, most recent first
    current_experience = None
    history_experiences = []
    
    if portfolio and portfolio.experiences:
        # Convert string timestamps to datetime objects for sorting
        for exp in portfolio.experiences:
            if not hasattr(exp, 'created_at_dt'):
                try:
                    exp.created_at_dt = datetime.datetime.fromisoformat(exp.created_at)
                except (ValueError, TypeError):
                    # If parsing fails, use current time
                    exp.created_at_dt = datetime.datetime.now()
        
        # Sort experiences by created_at_dt in descending order (newest first)
        sorted_experiences = sorted(portfolio.experiences, key=lambda x: getattr(x, 'created_at_dt', datetime.datetime.now()), reverse=True)
        
        # The most recent experience is the current one
        if sorted_experiences:
            current_experience = sorted_experiences[0]
            # All other experiences are history
            history_experiences = sorted_experiences[1:]
    
    # Get theme preference (default to 'professional' if not set)
    theme = portfolio.theme if portfolio and portfolio.theme else 'professional'
    
    return render_template('portfolio.html', portfolio=portfolio, current_experience=current_experience, history_experiences=history_experiences, theme=theme)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

@app.route('/set_theme/<theme>')
@login_required
def set_theme(theme):
    # Validate theme
    valid_themes = ['default', 'dark', 'nature', 'professional']
    if theme not in valid_themes:
        theme = 'professional'  # Default to professional if invalid
    
    # Update user's portfolio theme
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if portfolio:
        portfolio.theme = theme
        db.session.commit()
    
    # Redirect back to the referring page or portfolio
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('portfolio'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
        
    email = data['email']
    
    # Email validation
    email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    if not email_regex.match(email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400
    
    try:
        # Here you would typically save the email to a database or send it to a mailing service
        # For now, we'll just return success without sending an email
        
        # Log the subscription
        app.logger.info(f"Newsletter subscription from: {email}")
        
        # Uncomment this section when email sending is properly configured
        # msg = Message('Newsletter Subscription Confirmation', recipients=[email])
        # msg.body = f"Thank you for subscribing to our newsletter! You'll receive updates about new features and tips."
        # mail.send(msg)
        
        return jsonify({'success': True, 'message': 'Subscription successful'})
    except Exception as e:
        app.logger.error(f"Subscription error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred during subscription'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Register custom filters
@app.template_filter('extract_skills')
def extract_skills(text):
    """Extract skills from text using NLP"""
    if not text:
        return []
    
    # This is a simplified implementation
    # In a real application, you would use NLP libraries like spaCy or NLTK
    common_skills = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
        'HTML', 'CSS', 'SQL', 'NoSQL', 'React', 'Angular', 'Vue', 'Node.js', 'Django',
        'Flask', 'Spring', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Data Science',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'CI/CD', 'Agile', 'Scrum'
    ]
    
    found_skills = []
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    
    return found_skills

@app.template_filter('extract_keywords')
def extract_keywords(text):
    """Extract keywords from text for experience tags"""
    if not text:
        return []
    
    # Common keywords in professional experience
    common_keywords = [
        'Leadership', 'Management', 'Development', 'Design', 'Implementation', 'Analysis',
        'Strategy', 'Planning', 'Coordination', 'Communication', 'Collaboration', 'Innovation',
        'Problem-solving', 'Research', 'Testing', 'Deployment', 'Maintenance', 'Support',
        'Training', 'Mentoring', 'Optimization', 'Automation', 'Integration', 'Security',
        'Performance', 'Scalability', 'Reliability', 'Documentation', 'Presentation',
        'Client', 'Customer', 'Stakeholder', 'Team', 'Project', 'Product', 'Service',
        'Budget', 'Timeline', 'Deadline', 'Quality', 'Efficiency', 'Productivity',
        'Growth', 'Revenue', 'Cost', 'ROI', 'KPI', 'Metric', 'Goal', 'Objective',
        'Achievement', 'Success', 'Improvement', 'Enhancement', 'Transformation'
    ]
    
    # Add technical skills to keywords
    common_keywords.extend(extract_skills(text))
    
    found_keywords = []
    for keyword in common_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            found_keywords.append(keyword)
    
    return found_keywords

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)