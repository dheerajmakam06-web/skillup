from functools import wraps

from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from app import db
from models.industry import Company, IndustryDemand

bp = Blueprint('industry', __name__, url_prefix='/industry')


def industry_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get('user_role') != 'industry':
            flash('Industry accounts can publish skill demand.')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


@bp.route('/dashboard', methods=['GET', 'POST'])
@industry_required
def dashboard():
    company = Company.query.first()
    if request.method == 'POST':
        company_name = request.form.get('company_name') or 'My Company'
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name, industry=request.form.get('industry') or 'Technology',
                              location=request.form.get('location') or 'Not specified',
                              official_url=request.form.get('official_url') or None,
                              description='Industry demand published by an employer.')
            db.session.add(company)
            db.session.commit()
        elif request.form.get('official_url'):
            company.official_url = request.form.get('official_url')
        db.session.add(IndustryDemand(company_id=company.id, role=request.form.get('role'),
                                      skill_name=request.form.get('skill_name'),
                                      importance=request.form.get('importance') or 'required'))
        db.session.commit()
        flash('Industry skill demand updated')
    companies = Company.query.order_by(Company.name).all()
    return render_template('industry_dashboard.html', companies=companies, selected_company=company)


@bp.route('/demand')
def demand():
    return render_template('demand_directory.html', companies=Company.query.order_by(Company.name).all())