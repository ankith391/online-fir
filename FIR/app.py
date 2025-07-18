# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this for production!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fir_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

class FIR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complainant_name = db.Column(db.String(100), nullable=False)
    complainant_contact = db.Column(db.String(20), nullable=False)
    incident_date = db.Column(db.String(20), nullable=False)
    incident_location = db.Column(db.String(200), nullable=False)
    incident_description = db.Column(db.Text, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    fir_number = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f'<FIR {self.fir_number}>'

# Initialize database within application context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/file_fir', methods=['GET', 'POST'])
def file_fir():
    if request.method == 'POST':
        try:
            # Validate and get form data
            complainant_name = request.form.get('complainant_name', '').strip()
            complainant_contact = request.form.get('complainant_contact', '').strip()
            incident_date = request.form.get('incident_date', '').strip()
            incident_location = request.form.get('incident_location', '').strip()
            incident_description = request.form.get('incident_description', '').strip()

            if not all([complainant_name, complainant_contact, incident_date, incident_location, incident_description]):
                flash('All fields are required!', 'danger')
                return redirect(url_for('file_fir'))

            # Generate FIR number
            today = datetime.now()
            fir_count = FIR.query.filter(
                db.func.date(FIR.registration_date) == today.date()).count() + 1
            fir_number = f"{today.strftime('%Y%m%d')}-{fir_count:04d}"

            # Create and save FIR record
            new_fir = FIR(
                complainant_name=complainant_name,
                complainant_contact=complainant_contact,
                incident_date=incident_date,
                incident_location=incident_location,
                incident_description=incident_description,
                fir_number=fir_number
            )

            db.session.add(new_fir)
            db.session.commit()
            
            flash(f'FIR filed successfully! Your FIR number is: {fir_number}', 'success')
            return redirect(url_for('fir_status', fir_number=fir_number))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            app.logger.error(f'Error filing FIR: {str(e)}')

    return render_template('file_fir.html')

@app.route('/fir_status/<fir_number>')
def fir_status(fir_number):
    fir = FIR.query.filter_by(fir_number=fir_number).first()
    if fir:
        return render_template('fir_status.html', fir=fir)
    flash('FIR not found. Please check the FIR number.', 'danger')
    return redirect(url_for('home'))

@app.route('/track_fir', methods=['GET', 'POST'])
def track_fir():
    if request.method == 'POST':
        fir_number = request.form.get('fir_number', '').strip()
        if fir_number:
            return redirect(url_for('fir_status', fir_number=fir_number))
        flash('Please enter a valid FIR number', 'danger')
    return render_template('track_fir.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)