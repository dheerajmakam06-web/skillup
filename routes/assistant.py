import os

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint('assistant', __name__, url_prefix='/api')


def project_context():
    path = os.path.join(current_app.root_path, 'project_context.md')
    with open(path, encoding='utf-8') as context_file:
        return context_file.read()


TOPICS = [
    (('roadmap', 'course', 'specialization', 'module', 'topic', 'progress'),
     'The course roadmap is controlled by data/roadmaps.json and loaded by ai/roadmap_generator.py. The selected course and specialization are stored on StudentProfile. RoadmapProgress stores completion separately for each user, course, and module.'),
    (('login', 'register', 'password', 'authentication', 'logout'),
     'Authentication is implemented in routes/auth.py. Users are stored by the User model, passwords are hashed with Werkzeug, and the active user id is kept in the Flask session.'),
    (('resume', 'cv'),
     'Resume upload and extraction are handled by routes/student.py and ai/resume_parser.py. PDF, DOCX, and TXT files are parsed for contact details, projects, certifications, experience, and skills.'),
    (('company', 'matching', 'employer', 'demand'),
     'Company matching is implemented in ai/industry_matching.py. It compares student skills and profile context with Company and IndustryDemand records. Industry demand routes are in routes/industry.py.'),
    (('dashboard', 'student'),
     'The student dashboard is rendered by routes/student.py and templates/student_dashboard.html. It combines education guidance, readiness, career recommendations, resume status, and company matches.'),
    (('technology', 'stack', 'framework', 'library', 'project'),
     'SkillUp uses Python, Flask, Flask-SQLAlchemy, SQLite by default, Jinja templates, Bootstrap, custom CSS, and vanilla JavaScript. Resume extraction uses pypdf and python-docx.'),
    (('route', 'routes', 'file', 'architecture', 'where'),
     'The main route ownership is: app.py for setup and the public wizard; routes/auth.py for login and registration; routes/student.py for dashboard, profile, roadmap, progress, and resume; routes/career.py for career pages; routes/industry.py for demand; and routes/assistant.py for this assistant.'),
    (('add', 'new', 'modify', 'change'),
     'To add a course, add a top-level entry to data/roadmaps.json with description, estimated_time, and stages containing title, difficulty, topics, and project. Add it to the relevant course catalog if it should appear in selectors.'),
]


@bp.route('/assistant', methods=['POST'])
def ask():
    question = request.get_json(silent=True) or {}
    text = (question.get('question') or '').strip()
    if not text:
        return jsonify({'answer': 'Ask me about SkillUp routes, courses, roadmaps, progress, authentication, resumes, dashboards, companies, or deployment.'})
    normalized = text.lower()
    for keywords, answer in TOPICS:
        if any(keyword in normalized for keyword in keywords):
            return jsonify({'answer': answer})
    context = project_context()
    lines = [line.strip('# ').strip() for line in context.splitlines() if line.strip()]
    overview = ' '.join(lines[:4])
    return jsonify({'answer': f'I could not match that to a specific subsystem. {overview} Ask about the roadmap, course selection, progress, login, resume analysis, company matching, dashboard, or deployment.'})
