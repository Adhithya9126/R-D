import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def dashboard():
    conn = get_db_connection()
    # Simple stats for the dashboard
    total_journals = conn.execute('SELECT COUNT(*) FROM journals').fetchone()[0]
    conn.close()
    return render_template('dashboard.html', total_journals=total_journals)

@app.route('/add_journal', methods=('GET', 'POST'))
def add_journal():
    if request.method == 'POST':
        # 1. Get all form data matching the new schema
        data = (
            request.form.get('journal_status'),
            request.form.get('dept'),
            request.form.get('author_position'),
            request.form.get('author_name'),
            request.form.get('collaborative_authors'),
            request.form.get('paper_title'),
            request.form.get('publisher'),
            request.form.get('journal_name'),
            request.form.get('journal_scope'),
            request.form.get('vol_issue_page'),
            request.form.get('month_year'),
            request.form.get('issn'),
            1 if 'is_scopus' in request.form else 0,
            1 if 'is_sci' in request.form else 0,
            1 if 'is_wos' in request.form else 0,
            request.form.get('impact_factor'),
            request.form.get('citation_score'),
            request.form.get('sjr_rating'),
            request.form.get('h_index'),
            request.form.get('anna_univ_list'),
            request.form.get('preview_link'),
            request.form.get('home_page_link'),
            request.form.get('doi_link'),
            request.form.get('collab_scope'),
            request.form.get('collab_institution'),
            "" # Placeholder for filename
        )

        # 2. Handle File Upload
        proof_file = request.files.get('proof')
        filename = ""
        if proof_file and proof_file.filename != '':
            filename = secure_filename(proof_file.filename)
            proof_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Update the last item in the tuple with the filename
            data = data[:-1] + (filename,)

        # 3. Insert into DB
        conn = get_db_connection()
        conn.execute('''INSERT INTO journals (
            journal_status, department, author_position, author_name, collaborative_authors,
            paper_title, publisher, journal_name, journal_scope, vol_issue_page,
            month_year, issn_number, is_scopus, is_sci_scie_ssci, is_wos,
            impact_factor, citation_score, sjr_rating, h_index, anna_univ_list,
            preview_link, home_page_link, doi_link, collab_scope, collab_institution, proof_filename
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('view_journals'))

    return render_template('add_journal.html')

@app.route('/view_journals')
def view_journals():
    conn = get_db_connection()
    journals = conn.execute('SELECT * FROM journals').fetchall()
    conn.close()
    return render_template('view_journals.html', journals=journals)

if __name__ == '__main__':
    # Initialize DB if it doesn't exist
    if not os.path.exists('database.db'):
        init_db()
    app.run(debug=True)