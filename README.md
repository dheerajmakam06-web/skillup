# SKILLPATH AI - Prototype

This is a prototype Flask application for SKILLPATH AI – Adaptive Education-to-Career Roadmap & Industry Skill Alignment Platform.

 # SkillUp

 SkillUp is a Flask education-to-career platform that helps students connect their course, skills, learning roadmap, resume, and career opportunities.

 ## Features

 - Course and specialization-specific learning roadmaps
 - Roadmap stages, topics, projects, difficulty, and estimated learning time
 - Course-specific progress tracking
 - Student profile and skill selection
 - Resume analysis for PDF, DOCX, and TXT files
 - Career recommendations and job-readiness scoring
 - Company matching based on skills and employer demand
 - Industry demand directory
 - Project-aware SkillUp AI Assistant
 - Student, industry, teacher, institution, and admin demo accounts

 ## Technology

 - Python 3.13+
 - Flask and Flask-SQLAlchemy
 - SQLite by default
 - Jinja templates, Bootstrap, CSS, and vanilla JavaScript
 - pypdf and python-docx for resume extraction
 - Gunicorn for deployment

 ## Run Locally on Windows

 ```powershell
 python -m venv venv
 venv\Scripts\activate
 pip install -r requirements.txt
 python app.py
 ```

 Open `http://127.0.0.1:5000`.

 You can also run `run_host.bat` from the project folder.

 ## Demo Accounts

 | Role | Email | Password |
 | --- | --- | --- |
 | Student | student@demo.com | demo123 |
 | Teacher | teacher@demo.com | demo123 |
 | Institution | college@demo.com | demo123 |
 | Industry | industry@demo.com | demo123 |
 | Admin | admin@demo.com | admin123 |

 ## Course Roadmaps

 Roadmaps are stored in `data/roadmaps.json`. Each course defines its own description, estimated time, stages, topics, difficulty, and project.

 To add a course, add a new entry to `data/roadmaps.json` and add the course to the relevant catalog JSON file if it should appear in the course selector.

 Progress is stored separately for each user, course, and roadmap stage, so progress from one course does not appear in another course.

 ## Project Assistant

 The top-right SkillUp AI Assistant answers questions about the project architecture, routes, roadmap system, authentication, resume analysis, company matching, and deployment. Its verified project context is documented in `project_context.md`.

 ## Deploy on Render

 This project includes `render.yaml` with the required deployment configuration.

 1. Create or sign in to a Render account.
 2. Create a new Web Service from the GitHub repository.
 3. Select `dheerajmakam06-web/skillup`.
 4. Render uses:

 ```text
 Build command: pip install -r requirements.txt
 Start command: gunicorn --bind 0.0.0.0:$PORT app:app
 ```

 5. Add a production `SECRET_KEY` environment variable if you do not use the generated value.

 The default SQLite database is suitable for a prototype. For persistent production data, configure a managed database and set `DATABASE_URL`.

 ## Share the Project

 GitHub repository:

 https://github.com/dheerajmakam06-web/skillup

 After Render deployment, share the Render service URL with your teacher for the live application.

1. Create virtualenv and install requirements:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update if needed.

3. Run the app:

```bash
python app.py
```

Demo accounts (seeded):

- student@demo.com / demo123
- teacher@demo.com / demo123
- college@demo.com / demo123
- industry@demo.com / demo123
- admin@demo.com / admin123

This prototype includes core flows, seeded demo data, and a local recommendation engine.

## Open in a browser

From the `skillpath_ai` folder, double-click `run_host.bat`, or run:

```powershell
python app.py
```

Then open `http://127.0.0.1:5000` in the same computer. Do not open `http://0.0.0.0:5000`; that address tells Flask which interfaces to listen on and is not a browser destination.

To open it from another device on the same Wi-Fi, find the computer IPv4 address with `ipconfig`, then open `http://YOUR_IPV4_ADDRESS:5000`. Windows Firewall may ask permission for Python; allow it on Private networks.

For public hosting, set the platform's start command to:

```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```
