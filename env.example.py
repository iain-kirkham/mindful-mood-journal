"""
env.example.py — non-executing template for the MoodJournal project.

This file documents the environment variables the project expects.
Do not import this file from application code; copy the relevant
examples into `env.py` or set environment variables in your shell.

Examples (copy into `env.py` and edit values):

# DEBUG value
# os.environ.setdefault("DEBUG", "True")

# SECRET_KEY for Django
# os.environ.setdefault("SECRET_KEY", "replace-with-a-secret-key")

# Database parts (used to build DATABASE_URL in `env.py`)
# os.environ.setdefault("DB_NAME", "django_db")
# os.environ.setdefault("DB_USER", "journal_rw")
# os.environ.setdefault("DB_PASSWORD", "replace-with-strong-password")

# Or set a full DATABASE_URL instead of DB_* parts:
# os.environ.setdefault("DATABASE_URL", "postgres://user:pw@host:5432/dbname")

Keep sensitive values out of source control — use this file only as
documentation for the expected environment variables.
"""
