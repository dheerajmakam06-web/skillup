from flask import Blueprint, render_template, request, session
from models.user import User
from ai.recommender import career_matches
from models.career import Career
from models.skill import Skill

bp = Blueprint('career', __name__, url_prefix='/career')

CAREER_GUIDES = {
    'Machine Learning Engineer': {
        'summary': 'Build, evaluate, and deploy models that learn from data.',
        'steps': ['Strengthen Python, SQL, mathematics, and statistics.', 'Learn supervised and unsupervised machine learning with scikit-learn.', 'Build projects such as churn prediction, fraud detection, and recommendation systems.', 'Learn deep learning with TensorFlow or PyTorch.', 'Package and deploy a model with Git, Docker, and a cloud platform.', 'Publish a clear portfolio, practice technical interviews, and apply for internships or junior roles.'],
        'projects': ['Customer churn prediction', 'Fraud detection', 'Model deployment API'],
        'certifications': ['Machine learning fundamentals', 'Cloud or MLOps fundamentals']
    },
    'Data Analyst': {
        'summary': 'Turn business data into clear analysis and decisions.',
        'steps': ['Master Excel, SQL, data cleaning, and descriptive statistics.', 'Use Python with Pandas and NumPy for repeatable analysis.', 'Create dashboards with Power BI or Tableau.', 'Build projects from a real question, dataset, analysis, and recommendation.', 'Present insights clearly to a non-technical audience.', 'Create a portfolio and apply for analyst internships and entry-level roles.'],
        'projects': ['Sales performance dashboard', 'Customer churn analysis', 'Business case study'],
        'certifications': ['Google Data Analytics', 'Power BI fundamentals']
    },
    'Web Developer': {
        'summary': 'Design and build reliable, accessible experiences for the web.',
        'steps': ['Learn semantic HTML, modern CSS, responsive layouts, and accessibility.', 'Build interactive interfaces with JavaScript.', 'Learn a frontend framework such as React and understand browser APIs.', 'Build a backend with Python, Node.js, or another server framework.', 'Use SQL, Git, testing, and deployment for production-ready projects.', 'Publish three polished projects and prepare for frontend or full-stack interviews.'],
        'projects': ['Personal portfolio', 'E-commerce website', 'REST API with frontend'],
        'certifications': ['JavaScript fundamentals', 'Cloud deployment fundamentals']
    },
    'Data Scientist': {
        'summary': 'Use statistics, experimentation, and machine learning to solve complex problems.',
        'steps': ['Build strong foundations in Python, SQL, probability, and statistics.', 'Practice data cleaning, exploration, visualization, and feature engineering.', 'Train and evaluate models with scikit-learn.', 'Study experimentation, model interpretation, and responsible AI.', 'Build end-to-end projects with a written explanation of the decisions and limitations.', 'Create a portfolio, collaborate on real datasets, and prepare for case-study interviews.'],
        'projects': ['Customer churn prediction', 'Recommendation system', 'Demand forecasting'],
        'certifications': ['Google Data Analytics', 'Machine learning fundamentals']
    }
}

@bp.route('/explorer')
def explorer():
    careers = Career.query.all()
    recommendations = []
    if session.get('user_id'):
        user = User.query.get(session['user_id'])
        recommendations = career_matches(user.student_profile) if user and user.student_profile else []
    return render_template('career_explorer.html', careers=careers, recommendations=recommendations)

@bp.route('/<int:career_id>')
def detail(career_id):
    career = Career.query.get(career_id)
    if not career:
        return render_template('career_detail.html', career=None, guide=None), 404
    guide = CAREER_GUIDES.get(career.title, {
        'summary': career.description or 'Build the skills and experience required for this career.',
        'steps': ['Review the required skills.', 'Choose a practical project.', 'Build and document your portfolio.', 'Seek feedback and practical experience.', 'Prepare your resume and interview examples.', 'Apply through verified company career pages.'],
        'projects': [], 'certifications': []
    })
    profile_context = None
    recommendation = None
    if session.get('user_id'):
        user = User.query.get(session['user_id'])
        if user and user.student_profile:
            profile_context = user.student_profile
            recommendation = next((item for item in career_matches(profile_context) if item['career'].id == career.id), None)
            selected_context = ', '.join(filter(None, [profile_context.course, profile_context.branch, profile_context.career_goal, profile_context.interests]))
            if selected_context:
                guide = dict(guide)
                guide['summary'] = f"{guide['summary']} This version is tuned to your selected profile: {selected_context}."
                guide['steps'] = [f"Start from your selected profile context: {selected_context}."] + guide['steps']
    return render_template('career_detail.html', career=career, guide=guide,
                           profile=profile_context, recommendation=recommendation)
