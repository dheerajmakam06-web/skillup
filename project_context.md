# SkillUp Project Context

## Project
SkillUp is a Flask and SQLAlchemy education-to-career platform. Students select a course and specialization, view a course-specific learning roadmap, manage a profile, upload a resume, compare skills with company demand, and explore careers.

## Technology
- Python and Flask
- Flask-SQLAlchemy with SQLite by default
- Jinja templates, Bootstrap, and custom CSS
- Vanilla JavaScript for form controls and the assistant
- pypdf and python-docx for resume extraction
- Gunicorn for non-Windows deployment

## Entry Points and Routes
- `app.py`: application factory, database initialization, demo seeding, public roadmap wizard, and About route.
- `routes/auth.py`: register, login, logout, and account deletion.
- `routes/student.py`: dashboard, authenticated roadmap, roadmap progress, profile, skills, resume upload, resume analysis, companies, and company detail routes.
- `routes/career.py`: career explorer and career detail pages.
- `routes/industry.py`: industry dashboard and demand directory.
- `routes/assistant.py`: project-aware assistant API.

## Templates
- `templates/base.html`: shared layout, left navigation, top-right SkillUp assistant panel.
- `templates/roadmap.html`: authenticated course-specific roadmap and progress controls.
- `templates/roadmap_builder.html`: public four-step roadmap wizard.
- `templates/student_dashboard.html`: student overview, readiness, recommendations, resume and company matches.
- `templates/profile.html`: education, course, specialization, location, interests, skills, and resume forms.
- `templates/login.html` and `templates/register.html`: authentication UI.
- `templates/resume_analysis.html`: extracted resume information.
- `templates/company_matches.html`, `templates/company_detail.html`, `templates/demand_directory.html`, and `templates/industry_dashboard.html`: employer matching and demand features.

## Database Models
- `User`: identity, username, password hash, and role.
- `StudentProfile`: education, selected course, specialization, interests, career goal, resume data, and user link.
- `Skill` and `StudentSkill`: skill catalog and student skill levels.
- `Career` and `CareerSkill`: careers and required skills.
- `Company` and `IndustryDemand`: companies, roles, and requested skills.
- `RoadmapProgress`: user, course key, module key, completion state, and timestamps. Progress is isolated by course.

## Course and Roadmap System
- Course selections are stored in `StudentProfile.course` and `StudentProfile.branch`.
- Course and specialization choices are submitted by `templates/roadmap.html` to `routes/student.py`.
- Roadmaps are defined in `data/roadmaps.json`.
- `ai/roadmap_generator.py` normalizes course and specialization names, prefers a specialization-specific roadmap, then the parent course roadmap, and only uses legacy fallback data when a course is not yet in the catalog.
- Each roadmap has a description, estimated time, stages, topics, difficulty, and project.
- `RoadmapProgress` records are keyed by `user_id + course_key + module_key`.

## Resume and Matching
- `ai/resume_parser.py` extracts text, contact details, projects, certifications, and experience.
- `ai/industry_matching.py` compares student skills and profile context with company demands.
- `ai/recommender.py` ranks career matches and calculates job readiness.

## Assistant
The assistant is a local project-aware endpoint, not an external language model. It reads `project_context.md` and maps common questions to verified project areas. It can explain the roadmap files, course selection, progress model, authentication, dashboard, resume analysis, company matching, demand routes, technologies, and how to add a course. The assistant UI is rendered in `base.html` and calls `/api/assistant` using `static/js/assistant.js`.

## Adding a Course
Add a new top-level entry to `data/roadmaps.json` with `description`, `estimated_time`, and `stages`. Each stage should contain `title`, `difficulty`, `topics`, and `project`. Add the course to the relevant course catalog or branch list if students should be able to select it from the UI. No route rewrite is required.

## Deployment
Run locally with `python app.py` or `run_host.bat`. For a hosted Linux process use `gunicorn --bind 0.0.0.0:$PORT app:app`.
