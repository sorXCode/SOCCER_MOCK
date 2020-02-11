An API that serves the latest scores of fixtures of matches in a “**Mock Premier League**”

## User Types

There should be:

- **Admin accounts** which are used to
  - signup/login
  - manage teams (add, remove, edit, view)
  - create fixtures (add, remove, edit, view)
  - Generate unique links for fixture

- **Users accounts** who can
  - signup/login
  - view teams
  - view completed fixtures
  - view pending fixtures
  - robustly search fixtures/teams

- Only the search API should be available to the public.

## Authentication and Session Management
1. Use redis as your session store.
3. Authentication and Authorization for admin and user accounts should be done using `Bearer token` and `JWT`.

## Tools/Stack

- Rails / Django / Expressjs
- Postgres
- Redis
- Docker
- POSTMAN
- Any testing framework in the chosen language.

## Bonus

1. `containerization` using `docker`.
2. Thorough documentation using POSTMAN.
3. `web caching` API endpoints using `Redis`.
4. Implementing `rate limiting` for user account API access.

