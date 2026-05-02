from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from toon_db import ToonDB
from datetime import datetime
import os
import logging
from config import config_by_name

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
env = os.environ.get('FLASK_ENV', 'dev')
app.config.from_object(config_by_name[env])

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Database with config
db = ToonDB(filename=app.config['DATABASE_FILE'])

import re

def check_content_safety(text):
    """
    Checks for common coding special characters to prevent injection/code snippets.
    Removes the heavy LLM dependency.
    """
    # Define common coding characters that are restricted
    restricted_pattern = r'[<>{}\[\];&\\|]'
    
    if re.search(restricted_pattern, text):
        logger.warning(f"Restricted characters detected in input: {text[:50]}...")
        return False
    return True

@app.route('/')
def index():
    quotes = db.get_all_quotes()
    return render_template('index.html', quotes=quotes, current_user=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'guest':
            import uuid
            guest_name = f"Guest_{str(uuid.uuid4())[:6]}"
            db.create_user(guest_name, "", is_guest=True)
            session['username'] = guest_name
            session['is_guest'] = True
            logger.info(f"Guest login: {guest_name}")
            return redirect(url_for('index'))

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        if action == 'register':
            if db.create_user(username, password, is_guest=False):
                session['username'] = username
                session['is_guest'] = False
                logger.info(f"New user registered: {username}")
                return redirect(url_for('index'))
            else:
                flash("Username already exists.", "error")
        elif action == 'login':
            user = db.get_user(username)
            if user and user.get('password') == password:
                session['username'] = username
                session['is_guest'] = user.get('is_guest', False)
                logger.info(f"User logged in: {username}")
                return redirect(url_for('index'))
            else:
                flash("Invalid credentials.", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_quote():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if session.get('is_guest'):
        flash("Guests cannot add quotes.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        text = request.form.get('text')
        author = request.form.get('author')
        
        if not text or not author:
            flash("Quote and author are required.", "error")
            return redirect(url_for('add_quote'))

        if not check_content_safety(text):
            flash("Content rejected: Restricted coding characters detected (< > { } [ ] ; & \\ |).", "error")
            return redirect(url_for('add_quote'))
            
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add_quote(text, author, session['username'], date_str)
        flash("Quote added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add_quote.html')

@app.route('/like/<quote_id>', methods=['POST'])
def like_quote(quote_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    status, count = db.toggle_like(quote_id, session['username'])
    return jsonify({"status": status, "likes": count})

@app.route('/comment/<quote_id>', methods=['POST'])
def add_comment(quote_id):
    if 'username' not in session:
        flash("You must be logged in to comment.", "error")
        return redirect(url_for('index'))
    
    text = request.form.get('text')
    if not text:
        flash("Comment cannot be empty.", "error")
        return redirect(url_for('index'))
        
    if not check_content_safety(text):
        flash("Comment rejected: Restricted coding characters detected.", "error")
        return redirect(url_for('index'))
        
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add_comment(quote_id, text, session['username'], date_str)
    flash("Comment added successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure necessary folders exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run server
    # Use waitress for production-grade serving on Windows
    if os.environ.get('FLASK_ENV') == 'prod':
        from waitress import serve
        logger.info("Starting production server with waitress on port 5000...")
        serve(app, host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5000)
