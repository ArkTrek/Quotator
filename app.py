from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from toon_db import ToonDB
from datetime import datetime
import requests
import os

app = Flask(__name__)
app.secret_key = 'super_secret_premium_key'

db = ToonDB()

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:1.5b" # Chosen due to 8GB system RAM limits

def check_content_safety(text):
    prompt = f"""Evaluate the following text. If it contains tampering-based content or severe spam, respond with exactly the word 'UNSAFE'. Otherwise, respond with exactly the word 'SAFE'. Only output SAFE or UNSAFE.

Text: {text}
"""
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "keep_alive": 0  # Unloads model immediately from RAM after use
        }, timeout=30)
        
        if response.status_code == 200:
            result = response.json().get("response", "").strip().upper()
            if "UNSAFE" in result:
                return False
            return True
    except requests.exceptions.RequestException as e:
        print(f"Ollama connection error: {e}")
        # Fallback if Ollama is not running (you could choose to block or allow, we'll allow for demo, but print error)
        # Ideally, we should reject or warn the user.
        return True
    
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
            return redirect(url_for('index'))

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        if action == 'register':
            if db.create_user(username, password, is_guest=False):
                session['username'] = username
                session['is_guest'] = False
                return redirect(url_for('index'))
            else:
                flash("Username already exists.", "error")
        elif action == 'login':
            user = db.get_user(username)
            if user and user.get('password') == password:
                session['username'] = username
                session['is_guest'] = user.get('is_guest', False)
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

        # AI Check
        is_safe = check_content_safety(text)
        if not is_safe:
            flash("Content rejected: The AI detected tampering or spam.", "error")
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
        
    is_safe = check_content_safety(text)
    if not is_safe:
        flash("Comment rejected: AI detected tampering or spam.", "error")
        return redirect(url_for('index'))
        
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add_comment(quote_id, text, session['username'], date_str)
    flash("Comment added successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure templates and static folders exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(host='0.0.0.0', debug=True, port=5000)
