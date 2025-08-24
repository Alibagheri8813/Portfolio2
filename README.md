# Ultra Premium Portfolio (Django 4)

A modern, accessible, high-performance portfolio for a top-tier 17-year-old creator. Includes projects, blog, resume (PDF placeholder), testimonials, contact with AJAX + rate limiting, client-side search + server fallback, SEO, analytics placeholder, sitemaps, robots, and CI.

## Quickstart
```bash
git clone <your-repo-url> premium-portfolio
cd premium-portfolio
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Docker:
```bash
docker build -t premium-portfolio .
docker run -p 8000:8000 --env-file .env premium-portfolio
```

## Env Vars
- DJANGO_SECRET_KEY (required)
- ALLOWED_HOSTS (comma-separated)
- DJANGO_SETTINGS_MODULE (default config.settings.dev)
- EMAIL_* (optional)
- RECAPTCHA_* (optional)
- GA_MEASUREMENT_ID (optional)

## Lint & Test
```bash
pip install ruff && ruff check .
python manage.py test -v 2
npm i && npm run lint:js
```

## Deploy
- Use Dockerfile/Procfile, set env vars, run migrations.
- Ensure DEBUG=False and configure ALLOWED_HOSTS.