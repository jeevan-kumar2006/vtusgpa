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
                'error': 'No subjects provided.'
            }), 400
        
        total_credits = 0
        total_credit_points = 0
        valid_subjects = 0
        
        for subject in subjects:
            credits = subject.get('credits', 0)
            grade = subject.get('grade', '').upper()
            
            if credits and grade and grade in GRADE_POINTS:
                total_credits += credits
                total_credit_points += credits * GRADE_POINTS[grade]
                valid_subjects += 1
        
        if total_credits == 0:
            return jsonify({
                'success': False,
                'error': 'No valid subjects with credits found.'
            }), 400
        
        sgpa = total_credit_points / total_credits
        
        # Determine grade classification
        if sgpa >= 9:
            grade_class = 'Outstanding'
        elif sgpa >= 8:
            grade_class = 'Excellent'
        elif sgpa >= 7:
            grade_class = 'Very Good'
        elif sgpa >= 6:
            grade_class = 'Good'
        elif sgpa >= 5:
            grade_class = 'Satisfactory'
        else:
            grade_class = 'Needs Improvement'
        
        return jsonify({
            'success': True,
            'sgpa': round(sgpa, 2),
            'total_credits': total_credits,
            'credit_points': total_credit_points,
            'subject_count': valid_subjects,
            'grade_class': grade_class
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/grades', methods=['GET'])
def get_grade_info():
    """Return grade information"""
    return jsonify({
        'grades': [
            {'grade': 'O', 'points': 10, 'range': '90-100%', 'description': 'Outstanding'},
            {'grade': 'S', 'points': 9, 'range': '80-89%', 'description': 'Superior'},
            {'grade': 'A', 'points': 8, 'range': '70-79%', 'description': 'Excellent'},
            {'grade': 'B', 'points': 7, 'range': '60-69%', 'description': 'Very Good'},
            {'grade': 'C', 'points': 6, 'range': '50-59%', 'description': 'Good'},
            {'grade': 'D', 'points': 5, 'range': '45-49%', 'description': 'Satisfactory'},
            {'grade': 'F', 'points': 0, 'range': 'Below 45%', 'description': 'Fail'}
        ]
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'scheme': 'VTU 2022',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    # Get port from environment variable (for Codespaces) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Debug mode for development
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Simplified print statement to avoid syntax errors
    print("-------------------------------------------")
    print(" VTU SGPA Calculator - Backend Started ")
    print(f" Scheme: VTU 2022")
    print(f" Running on: http://localhost:{port}")
    print(" Press Ctrl+C to quit")
    print("-------------------------------------------")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
