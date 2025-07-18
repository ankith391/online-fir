# Online FIR System

A Flask-based web application for filing and tracking First Information Reports (FIRs) online.

![FIR System Screenshot](screenshot.png) <!-- Add a screenshot later -->

## Features

- File new FIRs with complainant details and incident information
- Automatic FIR number generation (YYYYMMDD-XXXX format)
- Track FIR status using unique reference number
- SQLite database storage
- Responsive web interface

## Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5/CSS
- Bootstrap (optional)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/online-fir-system.git
   cd online-fir-system

2.Create and activate virtual environment (recommended):


   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install dependencies:

pip install -r requirements.txt

4.Running the Application
 python app.py