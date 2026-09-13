import copy
import json
import os


ROADMAPS = {
    'B.Tech AI & Data Science': {
        'summary': 'Build strong foundations in programming, data, machine learning, and production AI systems.',
        'stages': [
            {'title': 'Foundation', 'duration': 'Semester 1', 'focus': 'Programming and mathematical thinking', 'skills': ['Python', 'C++', 'Git', 'Linear Algebra', 'Probability'], 'milestone': 'Build two Python mini-projects and publish them on GitHub.'},
            {'title': 'Data Foundations', 'duration': 'Semester 2', 'focus': 'Work with structured data and databases', 'skills': ['SQL', 'Pandas', 'Statistics', 'Data Visualization', 'Excel'], 'milestone': 'Complete an exploratory data analysis project with a written insight report.'},
            {'title': 'Machine Learning Core', 'duration': 'Year 2', 'focus': 'Train, evaluate, and explain predictive models', 'skills': ['Machine Learning', 'Feature Engineering', 'Model Evaluation', 'Scikit-learn', 'Problem Solving'], 'milestone': 'Create a supervised learning project with a reproducible notebook and evaluation metrics.'},
            {'title': 'Deep Learning and AI', 'duration': 'Year 3', 'focus': 'Neural networks and modern AI applications', 'skills': ['Deep Learning', 'NLP', 'Computer Vision', 'Generative AI', 'LLM'], 'milestone': 'Build and document an AI application that solves a practical problem.'},
            {'title': 'Production Engineering', 'duration': 'Year 3-4', 'focus': 'Deploy reliable models and services', 'skills': ['Docker', 'AWS', 'APIs', 'MLOps', 'Monitoring'], 'milestone': 'Deploy a trained model as a documented API using Docker.'},
            {'title': 'Portfolio and Industry Readiness', 'duration': 'Final year', 'focus': 'Demonstrate professional capability', 'skills': ['System Design', 'Communication', 'Teamwork', 'Technical Interviews', 'Resume Building'], 'milestone': 'Complete a capstone, internship, portfolio review, and mock interview.'}
        ]
    },
    'B.Tech CSE': {
        'summary': 'Progress from programming fundamentals to full-stack software engineering and deployment.',
        'stages': [
            {'title': 'Programming Foundations', 'duration': 'Year 1', 'focus': 'Problem solving and core programming', 'skills': ['C', 'C++', 'Python', 'Git', 'Problem Solving'], 'milestone': 'Solve 100 structured programming problems.'},
            {'title': 'Computer Science Core', 'duration': 'Year 1-2', 'focus': 'Understand how software systems work', 'skills': ['Data Structures', 'Algorithms', 'Operating Systems', 'Computer Networks', 'DBMS'], 'milestone': 'Build a database-backed application and explain its architecture.'},
            {'title': 'Web and Application Development', 'duration': 'Year 2-3', 'focus': 'Create usable, tested applications', 'skills': ['HTML', 'CSS', 'JavaScript', 'Backend', 'REST API', 'SQL'], 'milestone': 'Ship a full-stack application with authentication and deployment.'},
            {'title': 'Engineering Practice', 'duration': 'Year 3', 'focus': 'Build software collaboratively', 'skills': ['Testing', 'System Design', 'Cloud', 'Docker', 'Agile'], 'milestone': 'Contribute to a team project using issues, pull requests, and tests.'},
            {'title': 'Career Readiness', 'duration': 'Final year', 'focus': 'Connect projects to target roles', 'skills': ['Portfolio', 'Communication', 'Interview Preparation', 'Internship Experience'], 'milestone': 'Complete a capstone and two role-specific mock interviews.'}
        ]
    },
    'BCA': {
        'summary': 'Develop practical software skills through programming, databases, web development, and projects.',
        'stages': [
            {'title': 'Digital and Programming Basics', 'duration': 'Year 1', 'focus': 'Build confidence with code and computing', 'skills': ['Computer Basics', 'C', 'Python', 'Problem Solving', 'Git'], 'milestone': 'Build three small command-line applications.'},
            {'title': 'Web and Database Skills', 'duration': 'Year 1-2', 'focus': 'Create connected applications', 'skills': ['HTML', 'CSS', 'JavaScript', 'SQL', 'REST API'], 'milestone': 'Create a CRUD web app with a relational database.'},
            {'title': 'Professional Development', 'duration': 'Year 2-3', 'focus': 'Improve engineering quality and employability', 'skills': ['Testing', 'Backend', 'Cloud', 'Communication', 'Teamwork'], 'milestone': 'Deploy a portfolio project and complete an internship or client project.'}
        ]
    },
    'Data Science': {
        'summary': 'Learn to turn data into reliable analysis, predictive models, and business decisions.',
        'stages': [
            {'title': 'Statistics and Python', 'duration': 'Phase 1', 'focus': 'Build analytical foundations', 'skills': ['Python', 'Statistics', 'Pandas', 'SQL'], 'milestone': 'Analyze a public dataset and communicate three actionable findings.'},
            {'title': 'Machine Learning', 'duration': 'Phase 2', 'focus': 'Build and evaluate models', 'skills': ['Machine Learning', 'Feature Engineering', 'Model Evaluation', 'Git'], 'milestone': 'Complete an end-to-end prediction project.'},
            {'title': 'Advanced Data Practice', 'duration': 'Phase 3', 'focus': 'Work with scale and production constraints', 'skills': ['Deep Learning', 'Data Engineering', 'Cloud', 'MLOps', 'Visualization'], 'milestone': 'Publish a production-style portfolio project with documentation.'}
        ]
    }
}


def load_course_roadmaps():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'roadmaps.json')
    with open(path, encoding='utf-8') as data_file:
        return json.load(data_file)


COURSE_ROADMAPS = load_course_roadmaps()


def _normalize(value):
    return ''.join(character for character in (value or '').lower() if character.isalnum())


ROADMAP_ALIASES = {
    'btech': 'B.Tech CSE',
    'btechcse': 'B.Tech CSE',
    'computerscienceengineeringcse': 'B.Tech CSE',
    'bcomhonours': 'B.Com Honours',
    'bca': 'BCA',
    'datascience': 'Data Science',
    'machinelearning': 'Machine Learning',
    'webdevelopment': 'Web Development',
}


def _course_key(course, specialization=''):
    available = {_normalize(key): key for key in COURSE_ROADMAPS}
    for value in (specialization, course):
        normalized = _normalize(value)
        if normalized in available:
            return available[normalized]
        if normalized in ROADMAP_ALIASES and ROADMAP_ALIASES[normalized] in COURSE_ROADMAPS:
            return ROADMAP_ALIASES[normalized]
    return None


def _format_roadmap(course_key, definition):
    stages = []
    for index, stage in enumerate(definition.get('stages', []), 1):
        topics = list(stage.get('topics', []))
        stages.append({
            'key': f'{_normalize(course_key)}-stage-{index}',
            'title': stage['title'],
            'duration': stage.get('duration', f'Stage {index}'),
            'difficulty': stage.get('difficulty', 'Intermediate'),
            'focus': ', '.join(topics[:5]),
            'skills': topics,
            'topics': topics,
            'estimated_time': stage.get('estimated_time', '4-6 weeks'),
            'milestone': stage.get('project', 'Complete a practical exercise.'),
            'project': stage.get('project', 'Complete a practical exercise.'),
        })
    return {
        'course_key': course_key,
        'course_name': course_key,
        'summary': definition.get('description', ''),
        'description': definition.get('description', ''),
        'estimated_time': definition.get('estimated_time', 'Self-paced'),
        'stages': stages,
    }

DEFAULT_ROADMAP = {
    'summary': 'Start with foundational learning, explore interests, then build practical skills through projects and assessments.',
    'stages': [
        {'title': 'Foundation', 'duration': 'Current stage', 'focus': 'Core academic and digital skills', 'skills': ['Communication', 'Problem Solving', 'Digital Literacy'], 'milestone': 'Complete a learning activity and reflect on what you enjoyed.'},
        {'title': 'Exploration', 'duration': 'Next stage', 'focus': 'Try different subjects and skill areas', 'skills': ['Creativity', 'Teamwork', 'Critical Thinking'], 'milestone': 'Try two activities from different interest areas.'},
        {'title': 'Practice and Discovery', 'duration': 'Following stage', 'focus': 'Turn interests into demonstrated skills', 'skills': ['Projects', 'Communication', 'Research'], 'milestone': 'Complete a small project and record your learning.'}
    ]
}

COURSE_ALIASES = {
    'B.Tech / B.E.': 'B.Tech CSE',
    'B.Tech': 'B.Tech CSE',
    'B.E.': 'B.Tech CSE',
    'Computer Science Engineering (CSE)': 'B.Tech CSE',
    'Artificial Intelligence & Data Science (AI & DS)': 'B.Tech AI & Data Science',
    'Data Science': 'Data Science',
    'BCA Data Science': 'Data Science',
}

CAREER_ROADMAPS = {
    'Data Analyst': {
        'summary': 'Learn to turn business questions into clean datasets, clear dashboards, and defensible decisions.',
        'stages': [
            {'title': 'Spreadsheet and Data Literacy', 'duration': 'Phase 1', 'focus': 'Understand tables, formulas, data types, and business questions', 'skills': ['Excel', 'Data Cleaning', 'Business Metrics', 'Critical Thinking'], 'milestone': 'Clean a messy sales workbook and explain five useful findings.'},
            {'title': 'SQL Investigation', 'duration': 'Phase 2', 'focus': 'Query relational data and investigate trends', 'skills': ['SQL', 'Joins', 'Aggregations', 'Data Validation'], 'milestone': 'Answer stakeholder questions with documented SQL queries.'},
            {'title': 'Dashboard Storytelling', 'duration': 'Phase 3', 'focus': 'Communicate patterns with effective visualizations', 'skills': ['Power BI', 'Tableau', 'Data Visualization', 'Presentation'], 'milestone': 'Publish an interactive dashboard with a one-page decision brief.'},
            {'title': 'Analyst Portfolio', 'duration': 'Phase 4', 'focus': 'Practice requirements gathering and analytical communication', 'skills': ['Portfolio', 'Case Studies', 'Communication', 'Interview Preparation'], 'milestone': 'Complete two analyst case studies and present one to a mock stakeholder.'}
        ]
    },
    'Software Developer': {
        'summary': 'Build software by moving from algorithms and APIs to tested, deployed applications.',
        'stages': [
            {'title': 'Programming and Problem Solving', 'duration': 'Phase 1', 'focus': 'Learn syntax, data structures, and debugging habits', 'skills': ['Python', 'JavaScript', 'Data Structures', 'Git'], 'milestone': 'Solve 40 programming problems and publish three small applications.'},
            {'title': 'Web and API Development', 'duration': 'Phase 2', 'focus': 'Create useful applications with a backend and database', 'skills': ['HTML', 'CSS', 'REST APIs', 'SQL', 'Authentication'], 'milestone': 'Ship a CRUD application with login, tests, and documentation.'},
            {'title': 'Testing and Deployment', 'duration': 'Phase 3', 'focus': 'Make software reliable and accessible to users', 'skills': ['Testing', 'Docker', 'Cloud', 'CI/CD'], 'milestone': 'Deploy an application and add automated tests for its core workflow.'},
            {'title': 'Engineering Portfolio', 'duration': 'Phase 4', 'focus': 'Explain technical decisions and collaborate professionally', 'skills': ['System Design', 'Code Review', 'Communication', 'Interview Preparation'], 'milestone': 'Complete a capstone, portfolio review, and two technical mock interviews.'}
        ]
    }
}


def get_roadmap(course, interests=None, career_goal=None, skills=None, specialization=None):
    selected = (course or '').strip()
    roadmap_key = COURSE_ALIASES.get(selected, selected)
    data_key = _course_key(roadmap_key, specialization)
    if data_key:
        base = _format_roadmap(data_key, COURSE_ROADMAPS[data_key])
    else:
        base = copy.deepcopy(CAREER_ROADMAPS.get((career_goal or '').strip()) or ROADMAPS.get(roadmap_key) or DEFAULT_ROADMAP)
        base.setdefault('course_key', roadmap_key or 'exploration')
        base.setdefault('course_name', roadmap_key or 'Exploration')
        base.setdefault('description', base.get('summary', ''))
        base.setdefault('estimated_time', 'Self-paced')
        for index, stage in enumerate(base.get('stages', []), 1):
            stage.setdefault('key', f'{_normalize(base["course_key"])}-stage-{index}')
            stage.setdefault('topics', stage.get('skills', []))
            stage.setdefault('difficulty', 'Intermediate')
            stage.setdefault('project', stage.get('milestone', 'Complete a practical exercise.'))
    interest_list = [item.strip() for item in (interests or '').split(',') if item.strip()]
    skill_list = [item for item in (skills or []) if item]
    if not interest_list and not career_goal and not skill_list:
        return base
    customized = {**base, 'stages': [dict(stage, skills=list(stage['skills'])) for stage in base['stages']]}
    context = interest_list + ([career_goal] if career_goal else [])
    context_label = ', '.join(context[:3])
    if not data_key:
        customized['summary'] = f"A focused {roadmap_key or 'career'} plan shaped by {context_label}. Build evidence through the milestones below."
    if skill_list:
        customized['stages'][0]['skills'] = list(dict.fromkeys(skill_list[:5] + customized['stages'][0]['skills']))[:5]
        customized['stages'][0]['focus'] = 'Strengthen your existing skills before adding the next role-specific foundation.'
    if career_goal:
        customized['stages'][-1]['focus'] = f'Prepare specifically for {career_goal} through portfolio evidence and interviews.'
        customized['stages'][-1]['milestone'] = f'Complete a {career_goal} project, review your skill gaps, and prepare targeted applications.'
    return customized
