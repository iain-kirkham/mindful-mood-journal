# Quick Start Guide

## What's Been Set Up

Your Django project is now configured for:
- **PostgreSQL** database (with SQLite fallback for local development)
- **Heroku** deployment ready
- **Environment variable management** with python-decouple
- **Static files handling** with WhiteNoise
- **Production security** settings

## 5-Minute Local Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   For local SQLite development, you can leave `DATABASE_URL` commented out or use the default.

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` - you're done!

---

## Deploy to Heroku (10 minutes)

1. **Install Heroku CLI** if you haven't: https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Add free PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set environment variables:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY='your-secret-key-here'
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```
   
   Generate a secure SECRET_KEY:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Initialize Git and deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

7. **Create admin user on Heroku:**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **View your app:**
   ```bash
   heroku open
   ```

Done! Your app is live at `https://your-app-name.herokuapp.com`

---

## File Reference

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `Procfile` | Heroku process configuration |
| `runtime.txt` | Python version for Heroku |
| `.env.example` | Environment variables template |
| `.gitignore` | Files to exclude from Git |
| `DEPLOYMENT.md` | Detailed deployment guide |
| `MoodJournal/settings.py` | Updated for PostgreSQL & Heroku |

---

## Key Features Enabled

✅ PostgreSQL support with automatic fallback to SQLite  
✅ Environment variable management  
✅ Static files served with WhiteNoise  
✅ Automatic migrations on Heroku deployment  
✅ Production security settings (SSL, secure cookies)  
✅ Admin interface ready at `/admin`

---

## Next Steps

1. **Add your Django apps:**
   ```bash
   python manage.py startapp myapp
   ```

2. **Create models** in `myapp/models.py`

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Deploy changes:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push heroku main
   ```

---

## Useful Commands

```bash
# Local development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Heroku
heroku logs --tail              # View live logs
heroku run python manage.py ... # Run Django commands
heroku config                   # View env variables
heroku ps                       # View running processes
```

---

## Need Help?

- **Local Django issues:** Check `python manage.py runserver` output
- **Heroku deployment issues:** Run `heroku logs --tail`
- **Database issues:** Verify `DATABASE_URL` is set correctly
- **Static files missing:** Run `python manage.py collectstatic`

See `DEPLOYMENT.md` for detailed troubleshooting.