# Testing

## Table of Contents

- [Testing](#testing)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Integration tests (testcontainers)](#integration-tests-testcontainers)
  - [Environment variables used by tests](#environment-variables-used-by-tests)
  - [Run a local PostgreSQL for development (optional)](#run-a-local-postgresql-for-development-optional)
  - [Run the full test suite](#run-the-full-test-suite)
    - [Latest local test run](#latest-local-test-run)
  - [Manual testing](#manual-testing)
    - [HTML validation](#html-validation)
    - [CSS validation](#css-validation)
    - [Accessibility](#accessibility)
    - [Performance and Best Practices](#performance-and-best-practices)
    - [Python Validation PEP8](#python-validation-pep8)
    - [JavaScript Validation JSHint](#javascript-validation-jshint)
    - [User-story testing (manual)](#user-story-testing-manual)

## Overview

- Unit and integration tests use Django's built-in test runner.
- Integration tests exercise database-level constraints using `testcontainers`.
- Docker is required for `testcontainers` and is also used to run a local PostgreSQL instance during development.
- Frontend validation: HTML is validated with the W3C HTML validator, CSS with the W3C CSS validator, and JavaScript is linted with JSHint and manually tested in-browser.
- Python validation: Python code is checked with `flake8` and CI linting rules to enforce PEP8 and project standards.
- Performance and best-practices: Lighthouse audits were run and with high results for all metrics tested.
- User-story QA: Manual user-story testing was performed against the acceptance criteria the results are summarised in the User-story QA section.

## Integration tests (testcontainers)

- Ensure Docker is running locally.
- Tests requiring `testcontainers` will start PostgreSQL containers automatically; manual database provisioning is not required.

## Environment variables used by tests

- `DATABASE_URL` — Optional when using a manually provisioned database; `testcontainers` will create or override as needed.
- `SECRET_KEY` and `DEBUG` — Required by `env.py` and should be set for local testing.

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

## Run the full test suite

To run the full test suit just use the built in test runner from django and it will bootstrap the testcontainers automatically.

```bash
python manage.py test
```

### Latest local test run

```
--- Container Active on localhost:51618 ---
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

Ran 79 tests in 36.503s

OK
Destroying test database for alias 'default'...
```

## Manual testing

### HTML validation

I have validated my website in the [HTML W3C validator](https://validator.w3.org/) and found no errors:

![HTML validation](readme/html-validation.png)


### CSS validation

I have also validated my website in the [W3C CSS validator](https://jigsaw.w3.org/css-validator/) and found no errors:

![CSS Validation](readme/css-validation.png)

### Accessibility

I have also completed some accessibility testing this was performed using [WAVE](https://wave.webaim.org/) which came back with a total score of 10/10 and no major errors with accessiblity or colours.

![WAVE accessibility](readme/wave-a11y.png)


### Performance and Best Practices

I have used Lighthouse in Google chrome on my deployed heroku site so performance and scores all reflect that in the production environment, these returned no major issues on either platform as far as best practices, SEO, and accessibility go, just some minor performance loss on mobile.

![Lighthouse Desktop](readme/Lighthouse-desktop.png)

*Lighthouse — Desktop results*

![Lighthouse Mobile](readme/Lighthouse-mobile.png)

*Lighthouse — Mobile results*

| Device  | Performance | Accessibility | Best Practices |  SEO |
| ------- | ----------: | ------------: | -------------: | ---: |
| Desktop |         100 |           100 |            100 |  100 |
| Mobile  |          97 |           100 |            100 |  100 |


### Python Validation PEP8

I have validated my python code through the flake8 linter and I have also ran the code through the CI Python linter.
The inital checks on the python validation with pep8 did return issues related to line limits (79 characters) but have since been resolved, the application was then retested to check for regressions and passed.

![pep8 test](readme/pep8test.png)

### JavaScript Validation JSHint

I have validated all of my JavaScript code through the JSHint and have only got minor warnings back and no major errors.


![JSHint entries](readme/jshint-entries.png)

*JSHint - entries results*

![JSHint toast](readme/jshint-entries.png)

*JSHint - toast results*


### User-story testing (manual)

I have manually tested my user flows against the user stories which I had defined in the main read me, I have ensured that they reach the acceptance criteria, and also that the features mentioned function as intended, please see the table below for the user stories I have tested.

| User Story | Status | Notes |
| --- | :---: | --- |
| User registration | Passed | Tests passed |
| User login | Passed | Tests passed |
| User logout | Passed | Tests passed |
| Conditional navigation bar | Passed | Tests passed |
| Create journal entry | Passed | Tests passed |
| Gratitude items | Passed | Tests passed |
| Paginated entry list | Passed | Tests passed |
| Detailed entry view | Passed | Tests passed |
| Edit entry | Passed | Tests passed |
| Random inspirational quote | Passed | Tests passed |
| Responsive design | Passed | Tests passed |
| Data privacy | Passed | Tests passed |
| Django admin management | Passed | Tests passed |
| Delete entry with confirmation | Passed | Tests passed |
| Keyword search | Passed | Tests passed |
| Notifications | Passed | Tests passed |
| Backdating journal entries | Passed | Tests passed |
| Toast notifications for user feedback | Passed | Tests passed |

