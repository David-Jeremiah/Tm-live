# TM Live — Django Quote & Catalogue System

Professional sound & lighting package catalogue with budget calculator for TM Live Uganda.

## Setup (Local)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata catalogue/fixtures/initial_data.json
python manage.py createsuperuser
python manage.py runserver
```

Open: http://localhost:8000

## Admin login (dev default)
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `tmlive2025`
  (Change this immediately in production!)

## Pages
| URL | Page |
|-----|------|
| `/` | Homepage |
| `/catalogue/` | Browse all packages |
| `/calculator/` | Budget calculator |
| `/quote/` | Request a quote |
| `/admin/` | Admin panel |

## Budget Calculator
Client enters their budget (e.g. 2,000,000 UGX) and the system:
1. Shows all **sound packages** within budget
2. Shows all **lighting packages** within budget
3. Suggests the best **sound + lighting combinations** that fit together

## Admin Features
- Add / edit / deactivate packages
- View all quote requests
- Update quote status (Draft → Sent → Accepted / Declined)

## Deployment (Railway / Render / PythonAnywhere)
1. Set `DEBUG=False` in settings.py
2. Set a real `SECRET_KEY`
3. Configure your database (PostgreSQL recommended)
4. Run `python manage.py collectstatic`
