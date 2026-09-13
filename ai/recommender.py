from models.skill import Skill, StudentSkill
from models.career import Career, CareerSkill
from app import db


def career_matches(profile):
    """Rank careers using the student's selected goal, interests, education, and skills."""
    selected_skills = {item.skill.name.lower() for item in profile.skills if item.level > 0}
    goal = (profile.career_goal or '').lower()
    interests = (profile.interests or '').lower()
    context = ' '.join(filter(None, [profile.education_level, profile.course, profile.branch])).lower()
    results = []
    for career in Career.query.all():
        required = [item.skill_name for item in career.skills]
        matched = [skill for skill in required if skill.lower() in selected_skills]
        skill_score = (len(matched) / len(required) * 70) if required else 0
        goal_score = 20 if goal and (goal == career.title.lower() or career.title.lower() in goal or goal in career.title.lower()) else 0
        career_context = f'{career.title} {career.description or ""}'.lower()
        interest_score = 10 if interests and any(term.strip() in career_context for term in interests.split(',')) else 0
        education_score = 5 if context and any(term in career_context for term in context.split()) else 0
        score = min(100, round(skill_score + goal_score + interest_score + education_score))
        results.append({'career': career, 'match_percent': score, 'matched_skills': matched,
                        'missing_skills': [skill for skill in required if skill not in matched]})
    return sorted(results, key=lambda item: (-item['match_percent'], item['career'].title))

def recommend_for_student(profile, career):
    # Gather student's verified or present skills
    student_skills = {s.skill.name: s.level for s in profile.skills}
    career_reqs = [(cs.skill_name, cs.weight) for cs in career.skills]
    matched = []
    missing = []
    total_weight = sum(w for _,w in career_reqs) if career_reqs else 1
    matched_weight = 0.0
    for name, weight in career_reqs:
        if name in student_skills and student_skills[name] > 0:
            matched.append(name)
            matched_weight += weight
        else:
            missing.append(name)
    match_percent = int((matched_weight / total_weight)*100)
    recommendations = []
    # rank missing by assumed importance order (weight)
    for name, weight in sorted(career_reqs, key=lambda x: -x[1]):
        if name in missing:
            recommendations.append({'skill': name, 'priority': 'High' if weight>1 else 'Medium'})
    result = {
        'career': career.title,
        'matched_skills': matched,
        'missing_skills': missing,
        'match_percent': match_percent,
        'recommendations': recommendations
    }
    return result


def job_readiness_for_student(profile):
    # Very simple heuristic combining verified skill levels and number of projects (not implemented)
    skills = profile.skills
    if not skills:
        return {'overall': 20, 'breakdown': {}}
    total = 0
    max_total = 5 * len(skills)
    for s in skills:
        total += s.level
    overall = int((total / max_total) * 100)
    if overall < 10:
        overall = max(overall, 10)
    breakdown = {
        'Technical Skills': overall,
        'Practical Projects': min(80, overall+10),
        'Problem Solving': min(80, overall),
        'Communication': min(70, overall)
    }
    return {'overall': overall, 'breakdown': breakdown}
