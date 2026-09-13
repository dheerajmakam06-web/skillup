import json
import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from werkzeug.utils import secure_filename
from app import db
from models.user import User
from models.student import StudentProfile
from models.skill import Skill, StudentSkill
from models.career import Career
from ai.recommender import career_matches, recommend_for_student, job_readiness_for_student
from ai.roadmap_generator import get_roadmap, ROADMAPS, COURSE_ROADMAPS
from models.roadmap import RoadmapProgress
from ai.education_guidance import get_guidance, get_required_studies
from ai.industry_matching import company_matches, extract_resume_skills, group_company_matches
from ai.resume_parser import ALLOWED_EXTENSIONS, extract_resume_profile, extract_text
from ai.course_options import INTEREST_OPTIONS

bp = Blueprint('student', __name__, url_prefix='/student')


def load_json(filename):
    with open(os.path.join(current_app.root_path, 'data', filename), encoding='utf-8') as data_file:
        return json.load(data_file)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*a, **kw):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*a, **kw)
    return wrapped

@bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    # compute basic readiness if student
    readiness = None
    if profile:
        readiness = job_readiness_for_student(profile)
    guidance = get_guidance(profile.starting_class if profile else None)
    selected_skills = [item.skill.name for item in profile.skills if item.level > 0] if profile else []
    roadmap = get_roadmap(profile.course or profile.branch if profile else '', profile.interests if profile else '', profile.career_goal if profile else '', selected_skills, profile.branch if profile else '')
    required_studies = get_required_studies(profile.starting_class if profile else None, roadmap)
    matches = company_matches(profile) if profile else []
    company_groups = group_company_matches(matches)
    best_match = matches[0] if matches else None
    career_recommendations = career_matches(profile) if profile else []
    resume_analysis = {
        'uploaded': bool(profile and profile.resume),
        'filename': profile.resume if profile else None,
        'skills': sorted({item.skill.name for item in profile.skills if item.level > 0}) if profile else [],
    }
    return render_template('student_dashboard.html', user=user, profile=profile,
                           readiness=readiness, guidance=guidance, matches=matches,
                           required_studies=required_studies, company_groups=company_groups,
                           resume_analysis=resume_analysis, best_match=best_match,
                           career_recommendations=career_recommendations)

@bp.route('/roadmap', methods=['GET', 'POST'])
@login_required
def roadmap():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    if request.method == 'POST':
        profile.course = request.form.get('course') or profile.course
        profile.branch = request.form.get('branch', '').strip()
        db.session.commit()
        flash('Roadmap updated for your selected course.')
        return redirect(url_for('student.roadmap'))
    course = profile.course or profile.branch if profile else ''
    selected_skills = [item.skill.name for item in profile.skills if item.level > 0] if profile else []
    roadmap_data = get_roadmap(course, profile.interests if profile else '', profile.career_goal if profile else '', selected_skills, profile.branch if profile else '')
    guidance = get_guidance(profile.starting_class if profile else None)
    progress_rows = RoadmapProgress.query.filter_by(user_id=user.id, course_key=roadmap_data['course_key']).all()
    completed_modules = {row.module_key for row in progress_rows if row.completed}
    total_modules = len(roadmap_data.get('stages', []))
    completed_count = len(completed_modules)
    progress_percent = round((completed_count / total_modules) * 100) if total_modules else 0
    next_stage = next((stage for stage in roadmap_data.get('stages', []) if stage['key'] not in completed_modules), None)
    return render_template('roadmap.html', profile=profile, course=course,
                           roadmap=roadmap_data, guidance=guidance,
                           available_courses=sorted(COURSE_ROADMAPS.keys() | set(ROADMAPS.keys())),
                           course_branches=load_json('course_branches.json'),
                           completed_modules=completed_modules,
                           progress_percent=progress_percent,
                           next_stage=next_stage)

@bp.route('/roadmap/progress', methods=['POST'])
@login_required
def roadmap_progress():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    current_course = profile.course or profile.branch if profile else ''
    roadmap_data = get_roadmap(current_course, profile.interests if profile else '', profile.career_goal if profile else '', specialization=profile.branch if profile else '')
    module_key = request.form.get('module_key', '').strip()
    valid_modules = {stage['key'] for stage in roadmap_data.get('stages', [])}
    if module_key not in valid_modules:
        flash('That roadmap stage is not part of your current course.')
        return redirect(url_for('student.roadmap'))
    progress = RoadmapProgress.query.filter_by(user_id=user.id, course_key=roadmap_data['course_key'], module_key=module_key).first()
    if not progress:
        progress = RoadmapProgress(user_id=user.id, course_key=roadmap_data['course_key'], module_key=module_key)
        db.session.add(progress)
    progress.mark(request.form.get('completed') == 'on')
    db.session.commit()
    return redirect(url_for('student.roadmap'))

@bp.route('/after-studies', methods=['GET','POST'])
@login_required
def after_studies():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    careers = Career.query.all()
    selected = None
    result = None
    if request.method == 'POST':
        career_id = int(request.form.get('career_id'))
        selected = Career.query.get(career_id)
        result = recommend_for_student(profile, selected)
    return render_template('after_studies.html', careers=careers, selected=selected, result=result)

@bp.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    if request.method == 'POST':
        profile.education_level = request.form.get('education_level')
        profile.starting_class = request.form.get('starting_class') or profile.starting_class
        profile.institution = request.form.get('institution') or request.form.get('school')
        profile.school = profile.institution
        profile.state = request.form.get('state')
        profile.district = request.form.get('district')
        profile.city = request.form.get('city')
        profile.course = request.form.get('course')
        profile.branch = request.form.get('branch')
        profile.location = request.form.get('location')
        selected_interests = request.form.getlist('interests')
        profile.interests = ', '.join(selected_interests) if selected_interests else profile.interests
        profile.career_goal = request.form.get('career_goal') or profile.career_goal
        profile.study_stream = request.form.get('study_stream') or profile.study_stream
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('student.dashboard'))
    skills = Skill.query.order_by(Skill.name).all()
    return render_template('profile.html', profile=profile, skills=skills,
                           interest_options=INTEREST_OPTIONS,
                           education_levels=load_json('education_levels.json'),
                           locations=load_json('locations.json'),
                           institutions=load_json('institutions.json')['institutions'],
                           skill_catalog=load_json('skills.json'),
                           branches=load_json('branches.json'),
                           course_catalog=load_json('courses_catalog.json'),
                           interests_catalog=load_json('interests.json'),
                           career_goals=load_json('career_goals.json'),
                           course_branches=load_json('course_branches.json'),
                           courses=load_json('courses.json'))

@bp.route('/add-skill', methods=['POST'])
@login_required
def add_skill():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    posted_ids = request.form.getlist('skill_ids') or ([request.form.get('skill_id')] if request.form.get('skill_id') else [])
    posted_ids = list(dict.fromkeys(int(skill_id) for skill_id in posted_ids))
    if not 3 <= len(posted_ids) <= 20:
        flash('Please select between 3 and 20 skills.')
        return redirect(url_for('student.profile'))
    level = int(request.form.get('level', 1))
    profile.skills.clear()
    for skill_id in posted_ids:
        db.session.add(StudentSkill(profile_id=profile.id, skill_id=skill_id, level=level, verified=False))
    db.session.commit()
    flash('Skill added')
    return redirect(url_for('student.profile'))


@bp.route('/resume', methods=['POST'])
@login_required
def upload_resume():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    uploaded = request.files.get('resume')
    if not uploaded or not uploaded.filename:
        flash('Choose a resume file first')
        return redirect(url_for('student.profile'))
    extension = os.path.splitext(uploaded.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        flash('Upload a PDF, DOCX, or text resume')
        return redirect(url_for('student.profile'))
    filename = secure_filename(uploaded.filename)
    try:
        resume_text = extract_text(uploaded, extension)
    except (ValueError, ImportError, OSError):
        flash('We could not read that resume. Please check the file and try again.')
        return redirect(url_for('student.profile'))
    extracted = extract_resume_profile(resume_text)
    detected = extract_resume_skills(resume_text, Skill.query.all())
    existing = {item.skill_id for item in profile.skills}
    for skill in Skill.query.filter(Skill.name.in_(detected)).all():
        if skill.id not in existing:
            db.session.add(StudentSkill(profile_id=profile.id, skill_id=skill.id, level=3, verified=False))
    profile.resume = filename
    profile.resume_name = filename
    profile.extracted_name = extracted['name']
    profile.extracted_email = extracted['email']
    profile.extracted_phone = extracted['phone']
    profile.projects_text = '\n'.join(extracted['projects'])
    profile.extracted_skills_text = '\n'.join(detected)
    profile.certifications_text = '\n'.join(extracted['certifications'])
    profile.experience_text = '\n'.join(extracted['experience'])
    db.session.commit()
    flash(f'Resume uploaded. Detected {len(detected)} matching skills.')
    return redirect(url_for('student.resume_analysis'))


@bp.route('/resume-analysis')
@login_required
def resume_analysis():
    user = User.query.get(session['user_id'])
    profile = user.student_profile
    return render_template('resume_analysis.html', user=user, profile=profile,
                           extracted_skills=[item for item in (profile.extracted_skills_text or '').splitlines() if item],
                           projects=[item for item in (profile.projects_text or '').splitlines() if item],
                           certifications=[item for item in (profile.certifications_text or '').splitlines() if item],
                           experience=[item for item in (profile.experience_text or '').splitlines() if item])


@bp.route('/companies')
@login_required
def companies():
    user = User.query.get(session['user_id'])
    query = request.args.get('q', '').strip().lower()
    letter_filter = request.args.get('letter', '').strip().upper()
    matches = company_matches(user.student_profile)
    if query:
        matches = [match for match in matches if query in ' '.join([
            match['company'].name, match['company'].industry, match['role'],
            ' '.join(match['required']), match['company'].location or ''
        ]).lower()]
    if letter_filter:
        matches = [match for match in matches if match['company'].name.upper().startswith(letter_filter)]
    return render_template('company_matches.html', matches=matches, query=query, letter_filter=letter_filter)


@bp.route('/companies/<int:company_id>')
@login_required
def company_detail(company_id):
    user = User.query.get(session['user_id'])
    selected_role = request.args.get('role')
    match = next((item for item in company_matches(user.student_profile)
                  if item['company'].id == company_id and (not selected_role or item['role'] == selected_role)), None)
    if not match:
        return redirect(url_for('student.companies'))
    return render_template('company_detail.html', match=match)
