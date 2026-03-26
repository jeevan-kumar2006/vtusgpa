// VTU 2022 Scheme SGPA Calculator

// Grade points mapping
const GRADE_POINTS = {
    'O': 10,
    'S': 9,
    'A': 8,
    'B': 7,
    'C': 6,
    'D': 5,
    'F': 0
};

// Default subjects for 2022 Scheme (CSE - can be customized per department)
const DEFAULT_SUBJECTS = {
    CSE: {
        1: [
            { name: 'Calculus and Linear Algebra', credits: 3 },
            { name: 'Physics', credits: 3 },
            { name: 'Basic Electrical Engineering', credits: 3 },
            { name: 'Elements of Civil Engineering', credits: 2 },
            { name: 'Programming for Problem Solving', credits: 3 },
            { name: 'Physics Lab', credits: 1 },
            { name: 'Electrical Lab', credits: 1 },
            { name: 'Programming Lab', credits: 1 }
        ],
        2: [
            { name: 'Advanced Calculus and Complex Analysis', credits: 3 },
            { name: 'Chemistry', credits: 3 },
            { name: 'Basic Electronics', credits: 3 },
            { name: 'Elements of Mechanical Engineering', credits: 2 },
            { name: 'Data Structures', credits: 3 },
            { name: 'Chemistry Lab', credits: 1 },
            { name: 'Electronics Lab', credits: 1 },
            { name: 'Data Structures Lab', credits: 1 }
        ],
        3: [
            { name: 'Discrete Mathematical Structures', credits: 3 },
            { name: 'Analog and Digital Electronics', credits: 4 },
            { name: 'Computer Organization', credits: 3 },
            { name: 'Object Oriented Programming with Java', credits: 3 },
            { name: 'Data Structures and Applications', credits: 3 },
            { name: 'Analog and Digital Lab', credits: 1 },
            { name: 'Java Lab', credits: 1 }
        ],
        4: [
            { name: 'Statistics and Probability', credits: 3 },
            { name: 'Design and Analysis of Algorithms', credits: 3 },
            { name: 'Microcontroller and Embedded Systems', credits: 3 },
            { name: 'Database Management Systems', credits: 3 },
            { name: 'Operating Systems', credits: 3 },
            { name: 'DBMS Lab', credits: 1 },
            { name: 'Algorithms Lab', credits: 1 },
            { name: 'Microcontroller Lab', credits: 1 }
        ]
    }
    // Add more departments as needed
};

// DOM Elements
let subjectsContainer;
let addSubjectBtn;
let calculateBtn;
let resultsSection;
let departmentSelect;
let semesterSelect;

// Counter for subject rows
let subjectCounter = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Initialize DOM references
    subjectsContainer = document.getElementById('subjectsContainer');
    addSubjectBtn = document.getElementById('addSubjectBtn');
    calculateBtn = document.getElementById('calculateBtn');
    resultsSection = document.getElementById('resultsSection');
    departmentSelect = document.getElementById('department');
    semesterSelect = document.getElementById('semester');

    // Event Listeners
    addSubjectBtn.addEventListener('click', () => addSubjectRow());
    calculateBtn.addEventListener('click', calculateSGPA);
    
    // Load default subjects when department/semester changes
    departmentSelect.addEventListener('change', loadDefaultSubjects);
    semesterSelect.addEventListener('change', loadDefaultSubjects);

    // Add initial subject rows
    for (let i = 0; i < 5; i++) {
        addSubjectRow();
    }

    // Entrance animations
    animateEntrance();
});

function animateEntrance() {
    const elements = document.querySelectorAll('.subject-row');
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.05}s`;
    });
}

function addSubjectRow(subject = null) {
    subjectCounter++;
    const row = document.createElement('div');
    row.className = 'subject-row';
    row.id = `subject-${subjectCounter}`;
    row.innerHTML = `
        <input type="text" class="subject-input" placeholder="Subject name" value="${subject ? subject.name : ''}">
        <input type="number" class="credit-input" placeholder="Credits" min="1" max="5" value="${subject ? subject.credits : ''}">
        <select class="grade-select">
            <option value="">Grade</option>
            <option value="O">O (10)</option>
            <option value="S">S (9)</option>
            <option value="A">A (8)</option>
            <option value="B">B (7)</option>
            <option value="C">C (6)</option>
            <option value="D">D (5)</option>
            <option value="F">F (0)</option>
        </select>
        <button type="button" class="btn-remove" onclick="removeSubjectRow(${subjectCounter})" aria-label="Remove subject">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    `;
    
    subjectsContainer.appendChild(row);
    
    // Scroll to new row
    row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function removeSubjectRow(id) {
    const row = document.getElementById(`subject-${id}`);
    if (row) {
        row.style.animation = 'fadeOut 0.2s ease forwards';
        setTimeout(() => {
            row.remove();
            updateResults();
        }, 200);
    }
}

// Add fadeOut keyframes dynamically
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateX(-20px);
        }
    }
`;
document.head.appendChild(styleSheet);

function loadDefaultSubjects() {
    const department = departmentSelect.value;
    const semester = semesterSelect.value;
    
    if (!department || !semester) return;
    
    // Clear existing subjects
    subjectsContainer.innerHTML = '';
    subjectCounter = 0;
    
    // Get subjects for selected department and semester
    const subjects = DEFAULT_SUBJECTS[department]?.[semester] || [];
    
    if (subjects.length > 0) {
        subjects.forEach(subject => {
            addSubjectRow(subject);
        });
        showToast(`Loaded ${subjects.length} subjects for ${department} Semester ${semester}`, 'success');
    } else {
        // Add empty rows if no predefined subjects
        for (let i = 0; i < 5; i++) {
            addSubjectRow();
        }
        showToast('Enter subjects manually or select a different combination', 'info');
    }
}

function calculateSGPA() {
    const rows = subjectsContainer.querySelectorAll('.subject-row');
    let totalCredits = 0;
    let totalCreditPoints = 0;
    let subjectCount = 0;
    let hasError = false;
    
    rows.forEach(row => {
        const credits = parseInt(row.querySelector('.credit-input').value) || 0;
        const grade = row.querySelector('.grade-select').value;
        
        if (credits > 0 && grade) {
            totalCredits += credits;
            totalCreditPoints += credits * GRADE_POINTS[grade];
            subjectCount++;
        } else if (credits > 0 || grade) {
            hasError = true;
        }
    });
    
    if (hasError) {
        showToast('Please fill in both credits and grades for all subjects', 'error');
        return;
    }
    
    if (subjectCount === 0) {
        showToast('Please add at least one subject with credits and grade', 'error');
        return;
    }
    
    const sgpa = totalCredits > 0 ? (totalCreditPoints / totalCredits).toFixed(2) : 0;
    
    // Update UI
    displayResults(sgpa, totalCredits, totalCreditPoints, subjectCount);
}

function displayResults(sgpa, credits, points, count) {
    resultsSection.classList.remove('hidden');
    
    // Animate the SGPA value
    const sgpaElement = document.getElementById('sgpaValue');
    animateValue(sgpaElement, 0, parseFloat(sgpa), 500);
    
    document.getElementById('totalCredits').textContent = credits;
    document.getElementById('creditPoints').textContent = points;
    document.getElementById('subjectCount').textContent = count;
    
    // Determine grade
    const gradeElement = document.getElementById('resultGrade');
    const gradeInfo = getGradeInfo(parseFloat(sgpa));
    gradeElement.textContent = gradeInfo.text;
    gradeElement.style.color = gradeInfo.color;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    showToast('SGPA calculated successfully', 'success');
}

function animateValue(element, start, end, duration) {
    const startTime = performance.now();
    const decimals = end % 1 !== 0 ? 2 : 0;
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeOut;
        
        element.textContent = current.toFixed(decimals);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function getGradeInfo(sgpa) {
    if (sgpa >= 9) return { text: 'Outstanding Performance', color: 'var(--grade-o)' };
    if (sgpa >= 8) return { text: 'Excellent Performance', color: 'var(--grade-s)' };
    if (sgpa >= 7) return { text: 'Very Good Performance', color: 'var(--grade-a)' };
    if (sgpa >= 6) return { text: 'Good Performance', color: 'var(--grade-b)' };
    if (sgpa >= 5) return { text: 'Satisfactory Performance', color: 'var(--grade-c)' };
    if (sgpa >= 4.5) return { text: 'Pass', color: 'var(--grade-d)' };
    return { text: 'Needs Improvement', color: 'var(--grade-f)' };
}

function updateResults() {
    // Recalculate when subjects are removed
    if (!resultsSection.classList.contains('hidden')) {
        calculateSGPA();
    }
}

function showToast(message, type = 'info') {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    
    // Remove after delay
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Real-time calculation preview (optional enhancement)
document.addEventListener('change', (e) => {
    if (e.target.classList.contains('credit-input') || e.target.classList.contains('grade-select')) {
        const rows = subjectsContainer.querySelectorAll('.subject-row');
        let allFilled = true;
        
        rows.forEach(row => {
            const credits = row.querySelector('.credit-input').value;
            const grade = row.querySelector('.grade-select').value;
            
            if ((credits && !grade) || (!credits && grade)) {
                allFilled = false;
            }
        });
        
        // Auto-calculate if all rows have both values
        if (allFilled && !resultsSection.classList.contains('hidden')) {
            calculateSGPA();
        }
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to calculate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        calculateSGPA();
    }
    
    // Ctrl/Cmd + N to add new subject
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        addSubjectRow();
    }
});
