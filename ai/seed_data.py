import json
import os

from app import db
from models.skill import Skill
from models.career import Career, CareerSkill
from models.industry import Company, IndustryDemand

SKILLS = [
    'Python','Java','C','C++','JavaScript','HTML','CSS','SQL','Excel','Power BI',
    'Statistics','Machine Learning','Deep Learning','NLP','Generative AI','LLM','RAG','AI Agents',
    'Docker','Kubernetes','AWS','Azure','Git','GitHub','MLOps','Data Engineering','Cybersecurity',
    'Communication','Leadership','Problem Solving','Teamwork','Pandas'
]

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'skills.json'), encoding='utf-8') as skills_file:
    SKILLS = sorted(set(SKILLS).union(skill for group in json.load(skills_file).values() for skill in group))

CAREERS = {
    'Machine Learning Engineer': ['Python','Statistics','Machine Learning','Deep Learning','Docker','Cloud','MLOps','Git'],
    'Data Analyst': ['Excel','SQL','Statistics','Python','Pandas','Power BI','Data Visualization'],
    'Web Developer': ['HTML','CSS','JavaScript','Git','Frontend Framework'],
    'Data Scientist': ['Python','Statistics','Machine Learning','Deep Learning','SQL','Pandas']
}

COMPANIES = {
    'Nova Analytics': {
        'industry': 'Data & AI', 'location': 'Bengaluru / Remote', 'category': 'startup', 'rating': 4.7,
        'roles': {'Junior Data Analyst': ['SQL', 'Excel', 'Statistics', 'Power BI'],
                  'AI Intern': ['Python', 'Machine Learning', 'Git', 'Communication']}
    },
    'Orbit Software Labs': {
        'industry': 'Software Product', 'location': 'Hyderabad / Remote', 'category': 'top_rated', 'rating': 4.8,
        'roles': {'Graduate Software Engineer': ['Python', 'JavaScript', 'SQL', 'Git', 'Problem Solving']}
    },
    'GreenGrid Technologies': {
        'industry': 'Climate Technology', 'location': 'Pune / Hybrid', 'category': 'startup', 'rating': 4.5,
        'roles': {'Data Engineering Intern': ['Python', 'SQL', 'Data Engineering', 'Docker']}
    },
    'Summit Systems': {
        'industry': 'Enterprise Technology', 'location': 'Chennai / Hybrid', 'category': 'established', 'rating': 4.3,
        'roles': {'Associate Software Engineer': ['Python', 'SQL', 'Git', 'Problem Solving']}
    }
}

# Demo opportunity directory: these records represent sample employer demand,
# training partners, and internship providers for the prototype.
EXPANDED_COMPANY_SPECS = [
    ('Aster Cloud', 'Cloud Services', 'Bengaluru', 'top_rated', 4.9, 'Cloud Engineering Trainee', ['Python', 'AWS', 'Docker', 'Git'], 'training', 'B.Tech CSE, B.Tech AI & Data Science'),
    ('BluePeak AI', 'Artificial Intelligence', 'Hyderabad', 'top_rated', 4.8, 'Machine Learning Engineer', ['Python', 'Machine Learning', 'Deep Learning', 'Git'], 'employment', 'B.Tech AI & Data Science, Data Science'),
    ('Cedar Digital', 'Software Product', 'Chennai', 'top_rated', 4.7, 'Frontend Developer Intern', ['HTML', 'CSS', 'JavaScript', 'Git'], 'internship', 'B.Tech CSE, BCA'),
    ('DeltaStack', 'Data Platforms', 'Bengaluru', 'top_rated', 4.8, 'Data Analyst', ['SQL', 'Python', 'Pandas', 'Power BI'], 'employment', 'Data Science, B.Tech AI & Data Science'),
    ('EastBridge Labs', 'Enterprise Technology', 'Hyderabad', 'top_rated', 4.6, 'Software Engineer Intern', ['Python', 'SQL', 'Git', 'Problem Solving'], 'internship', 'B.Tech CSE, BCA'),
    ('FluxNova', 'Product Engineering', 'Chennai', 'top_rated', 4.7, 'Full Stack Developer', ['HTML', 'CSS', 'JavaScript', 'SQL', 'Git'], 'employment', 'B.Tech CSE, BCA'),
    ('GraphGrid', 'Data & AI', 'Kadapa', 'top_rated', 4.6, 'Data Science Trainee', ['Python', 'Statistics', 'Pandas', 'SQL'], 'training', 'Data Science, B.Tech AI & Data Science'),
    ('HelioWorks', 'Renewable Technology', 'Pune', 'top_rated', 4.5, 'Data Engineering Intern', ['Python', 'SQL', 'Docker', 'Data Engineering'], 'internship', 'B.Tech AI & Data Science, B.Tech CSE'),
    ('Indigo Systems', 'Software Product', 'Mumbai', 'top_rated', 4.7, 'Graduate Software Engineer', ['Python', 'JavaScript', 'SQL', 'Git'], 'employment', 'B.Tech CSE, BCA'),
    ('Junction Analytics', 'Business Intelligence', 'Delhi', 'top_rated', 4.6, 'Business Data Analyst', ['Excel', 'SQL', 'Statistics', 'Power BI'], 'employment', 'Data Science'),
    ('Kite Labs', 'EdTech', 'Bengaluru', 'top_rated', 4.5, 'AI Product Intern', ['Python', 'Machine Learning', 'Communication'], 'internship', 'B.Tech AI & Data Science'),
    ('Lumen Secure', 'Cybersecurity', 'Hyderabad', 'top_rated', 4.6, 'Security Operations Trainee', ['Python', 'Linux', 'Cybersecurity', 'Communication'], 'training', 'B.Tech CSE, BCA'),
    ('MangoByte', 'Software Startup', 'Kadapa', 'startup', 4.4, 'Python Developer Intern', ['Python', 'Git', 'SQL', 'Problem Solving'], 'internship', 'B.Tech CSE, BCA'),
    ('NexaForge', 'AI Startup', 'Bengaluru', 'startup', 4.5, 'AI Research Intern', ['Python', 'Machine Learning', 'Statistics'], 'internship', 'B.Tech AI & Data Science, Data Science'),
    ('OpenOrbit', 'Cloud Startup', 'Hyderabad', 'startup', 4.3, 'DevOps Trainee', ['Docker', 'AWS', 'Git', 'Python'], 'training', 'B.Tech CSE'),
    ('PixelRoute', 'Design Technology', 'Chennai', 'startup', 4.2, 'Web Developer Intern', ['HTML', 'CSS', 'JavaScript'], 'internship', 'BCA, B.Tech CSE'),
    ('QuantaLeaf', 'Analytics Startup', 'Kadapa', 'startup', 4.4, 'Data Analyst Intern', ['Excel', 'SQL', 'Statistics', 'Power BI'], 'internship', 'Data Science'),
    ('RiverStack', 'SaaS Startup', 'Pune', 'startup', 4.3, 'Backend Developer', ['Python', 'SQL', 'Git', 'Docker'], 'employment', 'B.Tech CSE, BCA'),
    ('SkyMint', 'FinTech Startup', 'Mumbai', 'startup', 4.4, 'Risk Analytics Trainee', ['Python', 'Statistics', 'SQL', 'Excel'], 'training', 'Data Science'),
    ('TerraCode', 'Climate Technology', 'Bengaluru', 'startup', 4.5, 'Data Engineering Intern', ['Python', 'SQL', 'Data Engineering', 'Docker'], 'internship', 'B.Tech AI & Data Science'),
    ('UrbanLens', 'Retail Technology', 'Delhi', 'startup', 4.1, 'BI Developer Intern', ['SQL', 'Power BI', 'Excel'], 'internship', 'Data Science, BCA'),
    ('VividML', 'AI Startup', 'Hyderabad', 'startup', 4.6, 'Machine Learning Trainee', ['Python', 'Machine Learning', 'Git'], 'training', 'B.Tech AI & Data Science'),
    ('WaveNest', 'Health Technology', 'Chennai', 'startup', 4.3, 'Product Data Intern', ['Python', 'Pandas', 'SQL', 'Communication'], 'internship', 'Data Science'),
    ('Zenith Apps', 'Mobile Technology', 'Kadapa', 'startup', 4.2, 'Application Developer Intern', ['Java', 'SQL', 'Git', 'Problem Solving'], 'internship', 'B.Tech CSE, BCA'),
    ('SkillSpring Academy', 'Professional Training', 'Hyderabad', 'training', 4.8, 'Python and AI Training', ['Python', 'Machine Learning', 'Git'], 'training', 'B.Tech AI & Data Science, Data Science'),
    ('CodeHarbor Institute', 'Professional Training', 'Kadapa', 'training', 4.7, 'Full Stack Training', ['HTML', 'CSS', 'JavaScript', 'SQL'], 'training', 'B.Tech CSE, BCA'),
    ('DataMinds Hub', 'Professional Training', 'Bengaluru', 'training', 4.6, 'Data Analytics Bootcamp', ['Excel', 'SQL', 'Pandas', 'Power BI'], 'training', 'Data Science'),
    ('DevTrail Labs', 'Professional Training', 'Chennai', 'training', 4.5, 'Cloud and DevOps Training', ['AWS', 'Docker', 'Git', 'Python'], 'training', 'B.Tech CSE'),
    ('FutureReady Center', 'Professional Training', 'Pune', 'training', 4.4, 'Career Readiness Program', ['Communication', 'Problem Solving', 'Teamwork'], 'training', 'B.Tech CSE, BCA'),
    ('LearnLoop', 'Professional Training', 'Hyderabad', 'training', 4.6, 'Generative AI Training', ['Python', 'Generative AI', 'LLM'], 'training', 'B.Tech AI & Data Science'),
    ('NextSkill Works', 'Professional Training', 'Kadapa', 'training', 4.3, 'Web Development Training', ['HTML', 'CSS', 'JavaScript', 'Git'], 'training', 'BCA, B.Tech CSE'),
    ('Practical AI School', 'Professional Training', 'Bengaluru', 'training', 4.7, 'Applied ML Training', ['Python', 'Machine Learning', 'Statistics'], 'training', 'Data Science, B.Tech AI & Data Science'),
    ('SkillBridge Academy', 'Professional Training', 'Chennai', 'training', 4.5, 'Testing and QA Training', ['Python', 'Java', 'Problem Solving'], 'training', 'B.Tech CSE, BCA'),
    ('TechLift Institute', 'Professional Training', 'Mumbai', 'training', 4.4, 'Data Engineering Training', ['Python', 'SQL', 'Data Engineering', 'Docker'], 'training', 'B.Tech AI & Data Science'),
    ('Udaan Digital School', 'Professional Training', 'Delhi', 'training', 4.2, 'Digital Skills Foundation', ['Excel', 'Communication', 'Problem Solving'], 'training', 'BCA'),
    ('Vertex Learning', 'Professional Training', 'Kadapa', 'training', 4.3, 'Cloud Foundations', ['AWS', 'Git', 'Docker'], 'training', 'B.Tech CSE'),
    ('Aspire Internships', 'Career Internships', 'Hyderabad', 'internship', 4.5, 'Software Engineering Internship', ['Python', 'SQL', 'Git', 'Problem Solving'], 'internship', 'B.Tech CSE, BCA'),
    ('BuildWithUs', 'Career Internships', 'Kadapa', 'internship', 4.4, 'Web Development Internship', ['HTML', 'CSS', 'JavaScript', 'Git'], 'internship', 'BCA, B.Tech CSE'),
    ('CampusToCloud', 'Career Internships', 'Bengaluru', 'internship', 4.6, 'Cloud Internship', ['AWS', 'Docker', 'Python', 'Git'], 'internship', 'B.Tech CSE'),
    ('DataStart Careers', 'Career Internships', 'Chennai', 'internship', 4.5, 'Data Analyst Internship', ['SQL', 'Excel', 'Statistics', 'Power BI'], 'internship', 'Data Science'),
    ('EngineerLaunch', 'Career Internships', 'Hyderabad', 'internship', 4.3, 'Graduate Engineer Internship', ['Python', 'Java', 'Git', 'Communication'], 'internship', 'B.Tech CSE'),
    ('FirstRole Labs', 'Career Internships', 'Kadapa', 'internship', 4.2, 'AI Internship', ['Python', 'Machine Learning', 'Statistics'], 'internship', 'B.Tech AI & Data Science'),
    ('GradPath Technologies', 'Career Internships', 'Pune', 'internship', 4.4, 'Backend Internship', ['Python', 'SQL', 'Docker'], 'internship', 'B.Tech CSE, BCA'),
    ('InternOrbit', 'Career Internships', 'Bengaluru', 'internship', 4.6, 'Product Engineering Internship', ['JavaScript', 'HTML', 'CSS', 'Git'], 'internship', 'B.Tech CSE, BCA'),
    ('JobReady Analytics', 'Career Internships', 'Chennai', 'internship', 4.3, 'BI Internship', ['SQL', 'Excel', 'Power BI'], 'internship', 'Data Science'),
    ('LaunchPad AI', 'Career Internships', 'Hyderabad', 'internship', 4.7, 'Generative AI Internship', ['Python', 'Generative AI', 'LLM'], 'internship', 'B.Tech AI & Data Science'),
    ('MentorMesh', 'Career Internships', 'Kadapa', 'internship', 4.1, 'Technology Internship', ['Python', 'Communication', 'Teamwork'], 'internship', 'BCA, B.Tech CSE'),
    ('ProjectSpring', 'Career Internships', 'Bengaluru', 'internship', 4.5, 'Data Science Internship', ['Python', 'Pandas', 'Statistics', 'SQL'], 'internship', 'Data Science'),
    ('StartWorks', 'Career Internships', 'Chennai', 'internship', 4.2, 'Software Trainee Internship', ['C++', 'Python', 'Problem Solving', 'Git'], 'internship', 'B.Tech CSE')
]

for name, industry, location, category, rating, role, skills, opportunity_type, course_tags in EXPANDED_COMPANY_SPECS:
    COMPANIES[name] = {'industry': industry, 'location': location, 'category': category,
                       'rating': rating, 'roles': {role: skills},
                       'opportunity_type': opportunity_type, 'course_tags': course_tags}

def seed_demo_data():
    # skills
    for name in SKILLS:
        if not Skill.query.filter_by(name=name).first():
            db.session.add(Skill(name=name))
    db.session.commit()

    # careers
    for title, skills in CAREERS.items():
        c = Career.query.filter_by(title=title).first()
        if not c:
            c = Career(title=title, description=f"Career path for {title}")
            db.session.add(c)
            db.session.commit()

    for name, company_data in COMPANIES.items():
        company = Company.query.filter_by(name=name).first()
        if not company:
            company = Company(name=name, industry=company_data['industry'],
                              location=company_data['location'],
                              category=company_data.get('category', 'established'), rating=company_data.get('rating', 4.0),
                              opportunity_type=company_data.get('opportunity_type', 'employment'),
                              course_tags=company_data.get('course_tags', ''),
                              official_url=company_data.get('official_url'),
                              description='Hiring based on demonstrated, industry-relevant skills.')
            db.session.add(company)
            db.session.commit()
            for role, skills in company_data['roles'].items():
                for skill_name in skills:
                    db.session.add(IndustryDemand(company_id=company.id, role=role, skill_name=skill_name))
            db.session.commit()
        else:
            company.category = company_data.get('category', 'established')
            company.rating = company_data.get('rating', 4.0)
            company.opportunity_type = company_data.get('opportunity_type', 'employment')
            company.course_tags = company_data.get('course_tags', '')
            company.official_url = company_data.get('official_url')
            company.industry = company_data['industry']
            company.location = company_data['location']
            db.session.commit()
    for title, skills in CAREERS.items():
        career = Career.query.filter_by(title=title).first()
        if career and not career.skills:
            for skill_name in skills:
                db.session.add(CareerSkill(career_id=career.id, skill_name=skill_name, weight=1.0))
            db.session.commit()
