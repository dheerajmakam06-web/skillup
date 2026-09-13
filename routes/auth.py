import json
import os
import re

from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from app import db
from models.user import User
from models.student import StudentProfile
from models.skill import StudentSkill
from models.roadmap import RoadmapProgress
from ai.education_guidance import CLASS_OPTIONS, get_guidance

bp = Blueprint('auth', __name__)


def load_login_data(filename):
    with open(os.path.join(current_app.root_path, 'data', filename), encoding='utf-8') as data_file:
        return json.load(data_file)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        starting_class = request.form.get('starting_class') or 'college'
        if not name:
            flash('Please enter your name.')
            return redirect(url_for('auth.register'))
        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('Please enter a valid email.')
            return redirect(url_for('auth.register'))
        if not username:
            flash('Please enter a username.')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        if len(password) < 8:
            flash('Password must be at least 8 characters.')
            return redirect(url_for('auth.register'))
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.register'))
        u = User(name=name, email=email, username=username, role='student')
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        # create student profile for students
        profile = StudentProfile(user_id=u.id, starting_class=starting_class)
        db.session.add(profile)
        db.session.commit()
        flash('Account created successfully! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', class_options=CLASS_OPTIONS)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identity = request.form.get('identity', '').strip().lower()
        email = request.form.get('email', '').strip().lower() or identity
        password = request.form.get('password')
        starting_class = request.form.get('starting_class')
        education_level = request.form.get('education_level')
        starting_stage = request.form.get('starting_stage')
        course = request.form.get('course')
        branch = request.form.get('branch')
        career_goal = request.form.get('career_goal')
        user = User.query.filter((User.email == email) | (User.username == identity)).first()
        if user and password and user.check_password(password):
            if user.role == 'student' and user.student_profile:
                if starting_class:
                    user.student_profile.starting_class = starting_class
                if starting_stage:
                    user.student_profile.starting_class = starting_stage
                user.student_profile.education_level = education_level or user.student_profile.education_level
                user.student_profile.course = course or user.student_profile.course
                user.student_profile.branch = branch or user.student_profile.branch
                user.student_profile.career_goal = career_goal or user.student_profile.career_goal
                db.session.commit()
            session['user_id'] = user.id
            session['user_role'] = user.role
            session.permanent = True
            flash('Login successful!')
            if user.role == 'industry':
                return redirect(url_for('industry.dashboard'))
            return redirect(url_for('student.profile'))
        flash('Invalid username/email or password.')
    return render_template('login.html', class_options=CLASS_OPTIONS,
                           education_levels=load_login_data('education_levels.json'),
                           education_stages=load_login_data('education_stages.json'),
                           course_catalog=load_login_data('courses_catalog.json'),
                           branch_catalog=load_login_data('branches.json'),
                           career_goals=load_login_data('career_goals.json'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('auth.login'))

@bp.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    if request.method == 'POST':
        if request.form.get('confirmation') != 'DELETE':
            flash('Type DELETE to confirm account removal.')
            return redirect(url_for('auth.delete_account'))
        if user.student_profile:
            StudentSkill.query.filter_by(profile_id=user.student_profile.id).delete()
            db.session.delete(user.student_profile)
        RoadmapProgress.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        session.clear()
        flash('Your account has been deleted.')
        return redirect(url_for('auth.register'))
    return render_template('delete_account.html', user=user)
