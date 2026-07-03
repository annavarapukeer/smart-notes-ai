from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import os
from dotenv import load_dotenv
import sqlite3
import io
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ocr_engine import extract_text_from_image, extract_text_from_pdf
from ai_engine import process_notes_with_ai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super_secret_key_for_placements_project') 
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('smart_notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Database tables dynamic configuration verification setup
def init_analytics_db():
    conn = get_db_connection()
    # Schema checks to add tracking column if missing
    try:
        conn.execute('ALTER TABLE notes ADD COLUMN weak_areas TEXT DEFAULT ""')
        conn.commit()
    except sqlite3.OperationalError:
        pass # Column already exists
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('dashboard.html', notes=notes)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session: return redirect(url_for('login'))
    file = request.files['file']
    if file and file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        file_extension = file.filename.split('.')[-1].lower()
        raw_text = extract_text_from_pdf(filepath) if file_extension == 'pdf' else extract_text_from_image(filepath)
        ai_result = process_notes_with_ai(raw_text)
        
        conn = get_db_connection()
        conn.execute("INSERT INTO notes (user_id, filename, raw_text, summary, weak_areas) VALUES (?, ?, ?, ?, ?)", 
                     (session['user_id'], file.filename, raw_text, ai_result, "No tracking anomalies recorded yet."))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))

# --- NEW: Weak Area Processing API Route ---
@app.route('/log_performance', methods=['POST'])
def log_performance():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    note_id = data.get('note_id')
    status_msg = data.get('status')
    
    conn = get_db_connection()
    conn.execute('UPDATE notes SET weak_areas = ? WHERE id = ? AND user_id = ?', (status_msg, note_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/ask_document', methods=['POST'])
def ask_document():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    note_id = data.get('note_id')
    user_query = data.get('query')
    
    conn = get_db_connection()
    note = conn.execute('SELECT summary FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id'])).fetchone()
    conn.close()
    
    if not note: return jsonify({"error": "Context missing"}), 404
    
    # Strictly extract the CLEANED_TEXT block only to isolate the core knowledge base
    full_text = note['summary']
    context_segment = ""
    
    if '[CLEANED_TEXT]' in full_text and '[SUMMARY]' in full_text:
        context_segment = full_text.split('[CLEANED_TEXT]')[1].split('[SUMMARY]')[0].strip()
    else:
        # Fallback to general note data if tags are malformed or missing
        context_segment = full_text.split('[QUIZ]')[0].strip()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "API Key configuration missing on server"}), 500
        
    client = genai.Client(api_key=api_key)
    
    # Direct instruction to only use the cleaned textual reference data
    rag_prompt = f"""
    You are an expert AI Study Assistant. Answer the student's question based ONLY on the provided CLEANED TEXT context.
    If the answer cannot be found or logically inferred from this text, politely state that it's out of bounds.

    CLEANED TEXT CONTEXT:
    {context_segment}

    STUDENT QUESTION:
    {user_query}
    """
    
    try:
        response = client.models.generate_content(
            model='models/gemini-2.5-flash', 
            contents=rag_prompt
        )
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": f"AI Execution Error: {str(e)}"}), 500

@app.route('/download_pdf/<int:note_id>')
def download_pdf(note_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id'])).fetchone()
    conn.close()
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontSize=18, spaceAfter=20)
    body_style = ParagraphStyle('BStyle', parent=styles['Normal'], fontSize=11, leading=16)
    
    story.append(Paragraph(f"Smart Notes AI Study Asset Guide", title_style))
    story.append(Paragraph(f"<b>File Reference:</b> {note['filename']}", body_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(note['summary'].replace('\n', '<br/>'), body_style))
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"SmartNotes_{note_id}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
    init_analytics_db()
    app.run(debug=True)