import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Settings, Analysis
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from ai_engine import SportsAI
from sports_data import SportsData
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).limit(10).all()
    # Parse JSON results for display
    history = []
    for a in analyses:
        try:
            res = json.loads(a.result_json) if isinstance(a.result_json, str) else a.result_json
        except:
            res = {"error": "Invalid JSON", "raw": a.result_json}
        history.append({"analysis": a, "result": res})

    return render_template('dashboard.html', user=current_user, history=history)

@app.route('/api/matches/<sport>')
def get_matches(sport):
    sd = SportsData()
    matches = sd.get_matches(sport)
    return {"matches": matches}

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    settings = Settings.query.first()
    if not settings or (not settings.openai_api_key and not settings.gemini_api_key):
        flash('Por favor configura las API Keys en Admin primero.', 'error')
        return redirect(url_for('admin'))

    ai = SportsAI()
    input_type = 'text'
    input_content = ''

    # Handle Image Upload
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        input_type = 'image'
        input_content = filepath
    elif request.form.get('text_input'):
        input_type = 'text'
        input_content = request.form.get('text_input')
    else:
        flash('Debes subir una imagen o escribir texto.', 'error')
        return redirect(url_for('dashboard'))

    # Call AI
    result = ai.analyze(input_type, input_content, settings)

    # Save to DB
    analysis = Analysis(
        user_id=current_user.id,
        input_type=input_type,
        input_content=input_content if input_type == 'text' else os.path.basename(input_content),
        result_json=json.dumps(result)
    )
    db.session.add(analysis)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))

    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.openai_api_key = request.form.get('openai_key')
        settings.gemini_api_key = request.form.get('gemini_key')
        settings.default_provider = request.form.get('provider')
        settings.system_prompt = request.form.get('system_prompt')
        db.session.commit()
        flash('Configuración actualizada', 'success')

    return render_template('admin.html', settings=settings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
