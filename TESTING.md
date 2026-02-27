# Testing

This document describes how to run the test suite for MoodJournal.

## Overview

- Unit and integration tests use Django's built-in test runner.
- Integration tests exercise database-level constraints using `testcontainers`.
- Docker is required for `testcontainers` and is also used to run a local PostgreSQL instance during development.

## Run the full test suite

```bash
python manage.py test
```

## Integration tests (testcontainers)

- Ensure Docker is running locally.
- Tests that require `testcontainers` will start PostgreSQL containers automatically; no manual database provisioning is required.

## Run a local PostgreSQL for development (optional)

Use this minimal `docker-compose.yml` to run a local DB for manual testing or local development:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: moodjournal
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: moodjournal
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

- Update your local `DATABASE_URL`/`env.py` to point at `postgres://moodjournal:secret@localhost:5432/moodjournal` when using this compose file.

## Environment variables used by tests

- `DATABASE_URL` — optional when using a manually provisioned DB; `testcontainers` will create/override as needed.
- environment variables required by `env.py`  (`SECRET_KEY`, `DEBUG`) should be set for local testing.

## Manual testing

### HTML validation

I have validated my website in the HTML W3C validator and found no errors:

![HTML validation](readme/html-validation.png)


### CSS validation

I have also validated my website in the W3C CSS validator and found no errors:

![CSS Validation](readme/css-validation.png)

### Accessibility

I have also completed some accessibility testing this was performed using [WAVE](https://wave.webaim.org/) which came back with a total score of 10/10 and no major errors with accessiblity or colours.

![WAVE accessibility](readme/wave-a11y.png)


### Performance & Best Practices

I have used Lighthouse in Google chrome on my deployed heroku site so performance and scores all reflect that in the production environment, these returned no major issues on either platform as far as best practices, SEO, and accessibility go, just some minor performance loss on mobile.

Desktop

![Lighthouse Desktop](readme/Lighthouse-desktop.png)

Mobile

![Lighthouse Mobile](readme/Lighthouse-mobile.png)

| Device  | Performance | Accessibility | Best Practices |  SEO |
| ------- | ----------: | ------------: | -------------: | ---: |
| Desktop |         100 |           100 |            100 |  100 |
| Mobile  |          97 |           100 |            100 |  100 |

### User-story QA (manual)

- Walkthroughs: register, login/logout, create/edit/delete entry, search/filter, export CSV, and profile flows.
- Cross-browser: verify in latest Chrome, Firefox, and a mobile browser or emulated mobile viewport.
- Record: steps taken, observed behaviour, screenshots, and any console/network errors.

### Checklist & notes

- Keep a short checklist per user story and link manual test notes to failing automated tests or issues.
- Document environment details (browser versions, Docker/local DB state, env vars) to aid repro.
