"""
VTU SGPA Calculator Backend
Flask application for calculating SGPA based on VTU 2022 Scheme
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import os

app = Flask(__name__)
CORS(app)

# Grade points mapping for VTU 2022 Scheme
GRADE_POINTS = {
    'O': 10,  # Outstanding (90-100%)
    'S': 9,   # Superior (80-89%)
    'A': 8,   # Excellent (70-79%)
    'B': 7,   # Very Good (60-69%)
    'C': 6,   # Good (50-59%)
    'D': 5,   # Satisfactory (45-49%)
    'F': 0    # Fail (Below 45%)
}

# Get the parent directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / 'frontend'


@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory(FRONTEND_DIR, filename)


@app.route('/api/calculate', methods=['POST'])
def calculate_sgpa():
    """
    Calculate SGPA based on provided subjects
    
    Expected JSON payload:
    {
        "subjects": [
            {"name": "Subject 1", "credits": 3, "grade": "A"},
            {"name": "Subject 2", "credits": 4, "grade": "B"},
            ...
        ]
    }
    
    Returns:
    {
        "sgpa": 7.85,
        "total_credits": 20,
        "credit_points": 157,
        "subject_count": 5,
        "grade_class": "Very Good",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'subjects' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid request. Please provide subjects array.'
            }), 400
        
        subjects = data['subjects']
        
        if not subjects or len(subjects) == 0:
            return jsonify({
                'success': False,
                'error
