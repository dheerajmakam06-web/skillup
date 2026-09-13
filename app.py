from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
import json
import sys
from sqlalchemy import inspect, text
from config import Config
from ai.roadmap_generator import get_roadmap

db = SQLAlchemy()
sys.modules.setdefault('app', sys.modules[__name__])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    db.init_app(app)

    with app.app_context():
        from models import user, student, skill, career, industry, roadmap
        db.create_all()
        user_columns = {column['name'] for column in inspect(db.engine).get_columns('user')}
        if 'username' not in user_columns:
            with db.engine.begin() as connection:
                connection.execute(text('ALTER TABLE user ADD COLUMN username VARCHAR(64)'))
        # Keep existing prototype databases compatible after adding profile fields.
        if 'starting_class' not in {column['name'] for column in inspect(db.engine).get_columns('student_profile')}:
            with db.engine.begin() as connection:
                connection.execute(text('ALTER TABLE student_profile ADD COLUMN starting_class VARCHAR(32)'))
        student_columns = {column['name'] for column in inspect(db.engine).get_columns('student_profile')}
        if 'study_stream' not in student_columns:
            with db.engine.begin() as connection:
                connection.execute(text('ALTER TABLE student_profile ADD COLUMN study_stream VARCHAR(64)'))
        profile_columns = {
            'state': 'VARCHAR(128)',
            'district': 'VARCHAR(128)',
            'city': 'VARCHAR(128)',
            'institution': 'VARCHAR(256)',
            'course': 'VARCHAR(128)',
            'career_goal': 'VARCHAR(128)',
            'resume_name': 'VARCHAR(256)',
            'extracted_name': 'VARCHAR(128)',
            'extracted_email': 'VARCHAR(256)',
            'extracted_phone': 'VARCHAR(64)',
            'projects_text': 'TEXT',
            'extracted_skills_text': 'TEXT',
            'certifications_text': 'TEXT',
            'experience_text': 'TEXT',
        }
        with db.engine.begin() as connection:
            for column, column_type in profile_columns.items():
                if column not in student_columns:
                    connection.execute(text(f'ALTER TABLE student_profile ADD COLUMN {column} {column_type}'))
        company_columns = {column['name'] for column in inspect(db.engine).get_columns('company')}
        with db.engine.begin() as connection:
            if 'category' not in company_columns:
                connection.execute(text("ALTER TABLE company ADD COLUMN category VARCHAR(32) DEFAULT 'established'"))
            if 'rating' not in company_columns:
                connection.execute(text('ALTER TABLE company ADD COLUMN rating FLOAT DEFAULT 4.0'))
            if 'opportunity_type' not in company_columns:
                connection.execute(text("ALTER TABLE company ADD COLUMN opportunity_type VARCHAR(32) DEFAULT 'employment'"))
            if 'course_tags' not in company_columns:
                connection.execute(text('ALTER TABLE company ADD COLUMN course_tags VARCHAR(256)'))
            if 'official_url' not in company_columns:
                connection.execute(text('ALTER TABLE company ADD COLUMN official_url VARCHAR(512)'))
        from routes import auth, student as student_bp, career as career_bp
        app.register_blueprint(auth.bp)
        app.register_blueprint(student_bp.bp)
        app.register_blueprint(career_bp.bp)
        from routes import industry as industry_bp
        from routes import assistant as assistant_bp
        app.register_blueprint(industry_bp.bp)
        app.register_blueprint(assistant_bp.bp)
        from models.user import User
        from models.student import StudentProfile
        from ai.seed_data import seed_demo_data
        try:
            if not User.query.filter_by(email='admin@demo.com').first():
                admin = User(name='Admin', email='admin@demo.com', role='admin')
                admin.set_password('admin123')
                student_user = User(name='Rahul Kumar', email='student@demo.com', role='student')
                student_user.set_password('demo123')
                teacher = User(name='Demo Teacher', email='teacher@demo.com', role='teacher')
                teacher.set_password('demo123')
                inst = User(name='Demo Institution', email='college@demo.com', role='institution')
                inst.set_password('demo123')
                industry = User(name='Demo Industry', email='industry@demo.com', role='industry')
                industry.set_password('demo123')
                db.session.add_all([admin, student_user, teacher, inst, industry])
                db.session.commit()
            demo_student = User.query.filter_by(email='student@demo.com').first()
            if demo_student and not demo_student.student_profile:
                db.session.add(StudentProfile(
                    user_id=demo_student.id,
                    education_level='College / Higher Education',
                    branch='B.Tech AI & Data Science',
                    school='SkillPath Institute',
                    location='India'
                ))
                db.session.commit()
            elif demo_student and not demo_student.student_profile.starting_class:
                demo_student.student_profile.starting_class = 'college'
                db.session.commit()
            seed_demo_data()
        except IntegrityError:
            db.session.rollback()

    @app.route('/')
    def index():
        return redirect(url_for('auth.register'))

    @app.route('/roadmap', methods=['GET', 'POST'])
    def public_roadmap():
        data_dir = os.path.join(app.root_path, 'data')
        with open(os.path.join(data_dir, 'courses.json'), encoding='utf-8') as file:
            courses = json.load(file)
        with open(os.path.join(data_dir, 'branches.json'), encoding='utf-8') as file:
            branches = json.load(file)
        with open(os.path.join(data_dir, 'careers.json'), encoding='utf-8') as file:
            careers = json.load(file)
        if request.args.get('start') == '1':
            session.pop('roadmap_builder', None)
        selection = dict(session.get('roadmap_builder', {}))
        step = min(max(request.args.get('step', type=int) or 1, 1), 4)
        result = None
        errors = []
        if request.method == 'POST':
            step = min(max(request.form.get('step', type=int) or 1, 1), 4)
            selection.update({field: request.form.get(field, '').strip() for field in
                              ('stage', 'stream', 'course', 'location', 'interest', 'career', 'learning_style', 'learning_focus')
                              if field in request.form})
            required_by_step = {
                1: [('stage', 'Please select your education stage.')],
                2: [('course', 'Please select your course or branch.'),
                    ('location', 'Please enter your location.')],
                3: [('interest', 'Please select your interest.'),
                    ('career', 'Please select your career goal.')],
            }
            for field, message in required_by_step.get(step, []):
                if not selection.get(field):
                    errors.append(message)
            if not errors and step < 4:
                session['roadmap_builder'] = selection
                return redirect(url_for('public_roadmap', step=step + 1))
            if not errors and step == 4:
                session['roadmap_builder'] = selection
                course_text = selection['course'].lower()
                stream_text = selection.get('stream', '').lower()
                career = careers.get(selection['career'], {})
                if any(term in course_text for term in ('b.tech', 'b.e', 'engineering')) or 'engineering' in stream_text:
                    foundation = ['Mathematics and core subjects', 'Programming fundamentals', 'Data structures and problem solving']
                elif any(term in course_text for term in ('bca', 'mca', 'computer')):
                    foundation = ['Computing fundamentals', 'Programming and databases', 'Web application practice']
                elif any(term in course_text for term in ('b.sc', 'm.sc', 'data')) or 'science' in stream_text:
                    foundation = ['Quantitative foundations', 'Data collection and analysis', 'Research and visualization']
                elif any(term in course_text for term in ('mbbs', 'bds', 'nursing', 'pharm', 'medical')):
                    foundation = ['Life science foundations', 'Clinical and professional subjects', 'Ethics and practical training']
                else:
                    foundation = ['Core subjects for your course', 'Communication and digital literacy', 'Practical learning habits']
                learning_style = selection.get('learning_style') or 'a balanced mix of explanation and practice'
                learning_focus = selection.get('learning_focus') or 'projects'
                final_focus = f'Prepare for {selection["career"]} with {learning_style}, focused on {learning_focus}, portfolio evidence, interviews, and real-world practice.'
                result = {
                    'selection': selection,
                    'skills': career.get('skills', ['Communication', 'Problem Solving', 'Digital Literacy']),
                    'projects': career.get('projects', ['Build a portfolio project']),
                    'jobs': career.get('jobs', [selection['career']]),
                    'certifications': career.get('certifications', ['Industry fundamentals']),
                    'timeline': [
                        {'title': selection['stage'], 'focus': 'Understand your current level and set a realistic weekly study rhythm.', 'evidence': 'Create a simple study plan and complete one small learning activity.'},
                        {'title': foundation[0], 'focus': foundation[1], 'evidence': f'Finish the core lessons connected to {selection.get("stream") or selection["course"]}.'},
                        {'title': foundation[1], 'focus': foundation[2], 'evidence': f'Apply your learning to a small {selection["course"]} exercise.'},
                        {'title': 'Course foundations', 'focus': f'Build the important knowledge for {selection["course"]}.', 'evidence': f'Create notes and practice work for {selection["course"]}.'},
                        {'title': 'Role-ready skills', 'focus': ', '.join(career.get('skills', ['Communication', 'Problem Solving'])[:5]), 'evidence': f'Practice skills that support {selection["career"]}.'},
                        {'title': 'Projects and portfolio', 'focus': 'Turn learning into visible proof through projects.', 'evidence': '; '.join(career.get('projects', ['Build a portfolio project'])[:2])},
                        {'title': 'Certification and practical experience', 'focus': 'Use credentials, internships, labs, or volunteering to build confidence.', 'evidence': ', '.join(career.get('certifications', ['Industry fundamentals']))},
                        {'title': 'Career preparation', 'focus': final_focus, 'evidence': f'Prepare a resume, portfolio, and interview examples for {selection["career"]}.'},
                    ]
                }
                generated = get_roadmap(selection['course'], selection['interest'], selection['career'])
                result['timeline'] = [
                    {'title': stage['title'], 'focus': stage['focus'], 'evidence': stage['project']}
                    for stage in generated.get('stages', [])
                ]
                result['skills'] = [skill for stage in generated.get('stages', []) for skill in stage.get('topics', [])][:12]
                result['projects'] = [stage['project'] for stage in generated.get('stages', [])[:3]]
            step = 4
        return render_template('roadmap_builder.html', courses=courses, branches=branches,
                       careers=careers, result=result, errors=errors,
                       selection=selection, step=step)

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)), debug=True)
