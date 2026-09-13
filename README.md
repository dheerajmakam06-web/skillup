# SKILLPATH AI - Prototype

This is a prototype Flask application for SKILLPATH AI – Adaptive Education-to-Career Roadmap & Industry Skill Alignment Platform.

Run locally:

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
