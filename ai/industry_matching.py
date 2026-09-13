import re

from models.industry import Company


def extract_resume_skills(text, skills):
    normalized = re.sub(r'[^a-z0-9+#.]', ' ', (text or '').lower())
    found = []
    for skill in skills:
        pattern = r'(?<![a-z0-9])' + re.escape(skill.name.lower()) + r'(?![a-z0-9])'
        if re.search(pattern, normalized):
            found.append(skill.name)
    return found


def company_matches(profile):
    student_skills = {item.skill.name.lower() for item in profile.skills if item.level > 0}
    course = (profile.branch or '').lower()
    education = ' '.join(filter(None, [profile.education_level, profile.course, profile.branch])).lower()
    goal = (profile.career_goal or '').lower()
    interests = (profile.interests or '').lower()
    projects = (profile.projects_text or '').lower()
    certifications = (profile.certifications_text or '').lower()
    experience = (profile.experience_text or '').lower()
    matches = []
    for company in Company.query.order_by(Company.name).all():
        for role in sorted({d.role for d in company.demands}):
            required = [d.skill_name for d in company.demands if d.role == role]
            matched = [skill for skill in required if skill.lower() in student_skills]
            preferred = [d.skill_name for d in company.demands if d.role == role and d.importance == 'preferred']
            required_skills = [skill for skill in required if skill not in preferred]
            matched_required = [skill for skill in required_skills if skill.lower() in student_skills]
            skill_percent = int((len(matched_required) / len(required_skills)) * 100) if required_skills else 100
            course_match = bool(course and any(tag.strip().lower() in course for tag in (company.course_tags or '').split(',')))
            education_match = bool(education and any(tag.strip().lower() in education for tag in (company.course_tags or '').split(',')))
            goal_match = bool(goal and (goal in role.lower() or role.lower() in goal))
            interest_match = bool(interests and any(term.strip() in f'{company.industry} {role}'.lower() for term in interests.split(',')))
            project_match = min(100, 100 if projects and any(skill.lower() in projects for skill in required) else 0)
            education_percent = 100 if course_match or education_match else 0
            context_percent = 100 if goal_match else (50 if interest_match else 0)
            experience_match = 100 if not experience or 'fresher' in experience else 70
            certification_match = min(100, 100 if certifications and any(skill.lower() in certifications for skill in required) else 0)
            percent = round(skill_percent * .50 + project_match * .20 + education_percent * .15 + experience_match * .10 + certification_match * .05)
            percent = min(100, percent + round(context_percent * .05))
            matches.append({'company': company, 'role': role, 'required': required,
                            'matched': matched, 'missing': [s for s in required if s not in matched],
                            'match_percent': percent, 'skill_percent': skill_percent,
                            'project_percent': project_match, 'education_percent': education_percent,
                            'experience_percent': experience_match, 'certification_percent': certification_match,
                            'course_match': course_match, 'estimated': True})
    return sorted(matches, key=lambda item: (-item['match_percent'], -item['company'].rating, item['company'].name))


def group_company_matches(matches):
    groups = {'top_rated': [], 'startup': [], 'training': [], 'internship': [], 'established': []}
    for match in matches:
        category = match['company'].category or 'established'
        groups.setdefault(category, []).append(match)
    for group in groups.values():
        group.sort(key=lambda item: (-item['match_percent'], -item['company'].rating, item['company'].name))
    return groups