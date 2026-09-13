CLASS_OPTIONS = [
    ('class_1_5', 'Class 1-5'),
    ('class_6_10', 'Class 6-10'),
    ('class_11_12', 'Class 11-12'),
    ('college', 'College / Higher Education'),
    ('graduate', 'After Studies / Graduate'),
]

GUIDANCE = {
    'class_1_5': {
        'title': 'Foundation and Discovery',
        'description': 'Build confidence through core subjects, creativity, communication, and playful exploration. Career selection is not required at this stage.',
        'focus': ['Mathematics', 'Science discovery', 'Reading and English', 'Communication', 'Creativity', 'Digital literacy'],
        'next_step': 'Try activities from different subjects and notice current strengths and interests.'
    },
    'class_6_10': {
        'title': 'Interest and Skill Exploration',
        'description': 'Explore technology, science, creative work, business, and general skills before making stream decisions.',
        'focus': ['Coding basics', 'Experiments and research', 'Design and media', 'Financial literacy', 'Problem solving', 'Teamwork'],
        'next_step': 'Complete small projects in at least two different interest areas.'
    },
    'class_11_12': {
        'title': 'Stream and Career Exploration',
        'description': 'Understand stream options and compare several possible study and career paths. Your choices can continue to evolve.',
        'focus': ['Stream fundamentals', 'Career research', 'Entrance preparation', 'Communication', 'Project work', 'Digital skills'],
        'next_step': 'Compare three possible pathways using subjects, interests, and required skills.'
    },
    'college': {
        'title': 'Professional Skill Development',
        'description': 'Connect your course to practical industry skills, projects, assessments, internships, and verified evidence.',
        'focus': ['Course foundations', 'Industry tools', 'Projects', 'Internships', 'Assessments', 'Portfolio building'],
        'next_step': 'Choose one course-aligned project and one skill to practice this month.'
    },
    'graduate': {
        'title': 'Industry Alignment and Job Readiness',
        'description': 'Compare your demonstrated skills with target roles, close priority gaps, and build evidence through projects and practical experience.',
        'focus': ['Target role skills', 'Skill-gap analysis', 'Portfolio', 'Interview practice', 'Certifications', 'Industry experience'],
        'next_step': 'Select a target role and complete the highest-priority missing skill.'
    }
}


def get_guidance(starting_class):
    return GUIDANCE.get(starting_class, GUIDANCE['college'])


def get_required_studies(starting_class, roadmap=None):
    guidance = get_guidance(starting_class)
    if roadmap and roadmap.get('stages'):
        studies = []
        for stage in roadmap['stages'][:2]:
            studies.extend(stage['skills'])
        return studies
    return guidance['focus']
