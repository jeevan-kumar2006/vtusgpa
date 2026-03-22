from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Database of Subjects (Scheme -> Branch -> Sem -> Subjects)
# Credits are based on standard VTU structures.
CURRICULUM_DATA = {
    "2018": {
        "CSE": {
            "1": [{"code": "18CS51", "name": "Analysis of Algorithms", "credits": 4}],
            "2": [{"code": "18CS54", "name": "Computer Organization", "credits": 3}]
        },
        "ISE": { "1": [{"code": "18IS51", "name": "Algorithms", "credits": 4}] }
    },
    "2020": {
        "CSE": {
            "1": [{"code": "20CS41", "name": "Maths-IV", "credits": 3}, {"code": "20CS42", "name": "Analysis of Algorithms", "credits": 4}],
            "2": [{"code": "20CS51", "name": "Operating Systems", "credits": 4}]
        }
    },
    "2021": {
        "CSE": {
            "1": [
                {"code": "21CS51", "name": "Automata Theory", "credits": 3},
                {"code": "21CS52", "name": "Software Engineering", "credits": 3},
                {"code": "21CS53", "name": "Operating Systems", "credits": 4},
                {"code": "21CS54", "name": "Database Management", "credits": 4},
                {"code": "21CSL55", "name": "DB Lab", "credits": 1},
                {"code": "21CSL56", "name": "Algorithms Lab", "credits": 1}
            ],
            "2": [
                {"code": "21CS61", "name": "Computer Networks", "credits": 4},
                {"code": "21CS62", "name": "Computer Graphics", "credits": 3}
            ]
        },
        "ISE": {
            "1": [
                {"code": "21IS51", "name": "Information Security", "credits": 3},
                {"code": "21IS52", "name": "Web Tech", "credits": 4}
            ]
        },
        "ECE": { "1": [{"code": "21EC51", "name": "DSP", "credits": 4}] },
        "ME": { "1": [{"code": "21ME51", "name": "Turbo Machines", "credits": 4}] },
        "CIVIL": { "1": [{"code": "21CV51", "name": "Structural Analysis", "credits": 4}] }
    },
    "2022": {
        "CSE": {
            "1": [
                {"code": "22CS41", "name": "Maths-IV", "credits": 3},
                {"code": "22CS42", "name": "Analysis of Algorithms", "credits": 4},
                {"code": "22CS43", "name": "Operating Systems", "credits": 4}
            ],
            "2": [{"code": "22CS51", "name": "DBMS", "credits": 4}]
        },
        "ISE": { "1": [{"code": "22IS41", "name": "Algorithms", "credits": 4}] }
    },
    "2025": {
        "CSE": {
            "1": [
                {"code": "25CS11", "name": "Mathematics-I", "credits": 3},
                {"code": "25CS12", "name": "Physics", "credits": 3},
                {"code": "25CS13", "name": "Basics of Programming", "credits": 4}
            ],
            "2": [{"code": "25CS21", "name": "Mathematics-II", "credits": 3}]
        },
        "ISE": { "1": [{"code": "25IS11", "name": "Mathematics-I", "credits": 3}] },
        "ECE": { "1": [{"code": "25EC11", "name": "Mathematics-I", "credits": 3}] }
    }
}

# Default credits for manual add (common VTU structure)
DEFAULT_MANUAL_CREDITS = 4

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_branches', methods=['POST'])
def get_branches():
    scheme = request.json.get('scheme')
    branches = []
    if scheme in CURRICULUM_DATA:
        branches = sorted(list(CURRICULUM_DATA[scheme].keys()))
    
    # Add generic branches if not present in specific data, for manual entry support
    all_branches = sorted(list(set(branches + ['CSE', 'ISE', 'ECE', 'ME', 'CIVIL', 'EC', 'EE'])))
    return jsonify({'branches': all_branches})

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
    scheme = request.json.get('scheme')
    branch = request.json.get('branch')
    sem = request.json.get('sem')
    
    subjects = []
    if scheme in CURRICULUM_DATA:
        if branch in CURRICULUM_DATA[scheme]:
            if sem in CURRICULUM_DATA[scheme][branch]:
                subjects = CURRICULUM_DATA[scheme][branch][sem]
    
    return jsonify({'subjects': subjects})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json.get('subjects', [])
    total_credits = 0
    total_points = 0
    
    grade_map = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0}
    
    for sub in data:
        credits = int(sub.get('credits', 0))
        grade = sub.get('grade', '').upper()
        
        if grade in grade_map:
            points = grade_map[grade]
            total_credits += credits
            total_points += (credits * points)
    
    sgpa = 0
    if total_credits > 0:
        sgpa = round(total_points / total_credits, 2)
        
    return jsonify({'sgpa': sgpa})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
