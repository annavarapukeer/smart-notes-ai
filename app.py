from flask import Flask, render_template, request, redirect, url_for, session, flash,send_file
import os
import sqlite3
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ocr_engine import extract_text_from_image, extract_text_from_pdf
from ai_engine import process_notes_with_ai

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_placements_project' # Security Key
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('smart_notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
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
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Main Core Project Routes ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    # ఇక్కడ కేవలం లాగిన్ అయిన యూజర్ నోట్స్ మాత్రమే డేటాబేస్ నుండి వస్తాయి
    notes = conn.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('dashboard.html', notes=notes)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session: return redirect(url_for('login'))
    if 'file' not in request.files: return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '': return redirect(url_for('index'))

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        file_extension = file.filename.split('.')[-1].lower()
        raw_text = ""

        if file_extension == 'pdf':
            raw_text = extract_text_from_pdf(filepath)
        else:
            raw_text = extract_text_from_image(filepath)

        ai_result = process_notes_with_ai(raw_text)

        # ఇక్కడ యూజర్ ఐడి (session['user_id']) ని కూడా సేవ్ చేస్తున్నాం
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (user_id, filename, raw_text, summary) VALUES (?, ?, ?, ?)", 
                       (session['user_id'], file.filename, raw_text, ai_result))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
@app.route('/download_pdf/<int:note_id>')
def download_pdf(note_id):
    # 1. Login check (Security kosam)
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # 2. Database nundi note details tevali
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ? AND user_id = ?', 
                         (note_id, session['user_id'])).fetchone()
    conn.close()

    if not note:
        return "Note not found or access denied", 404

    # 3. PDF Buffer create cheyadam[cite: 1]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, spaceAfter=20)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=10)

    # 4. Content ni PDF lo add cheyadam[cite: 1]
    story.append(Paragraph(f"Smart Notes AI - Revision Material", title_style))
    story.append(Paragraph(f"<b>File:</b> {note['filename']}", body_style))
    story.append(Paragraph(f"<b>Date:</b> {note['created_at']}", body_style))
    story.append(Spacer(1, 15))
    
    # Summary and MCQs formatting[cite: 1]
    content_text = note['summary'].replace('\n', '<br/>')
    story.append(Paragraph(content_text, body_style))

    doc.build(story)
    buffer.seek(0)

    # 5. File ni download ki pampadam[cite: 1]
    return send_file(buffer, as_attachment=True, download_name=f"SmartNotes_{note_id}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)