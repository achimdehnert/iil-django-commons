# CLAUDE.md — iil-django-commons

Operating guide for an AI agent working in this repo. Repo-specific; the
user-level `~/.claude/CLAUDE.md` still applies and wins on conflicts.

## What this is

`iil-django-commons` (dist name `iil-django-commons`, import `iil_commons`) is
the platform's **shared backend services library** for Django Hub projects.
Implements [ADR-131](https://github.com/achimdehnert/platform/blob/main/docs/adr/ADR-131-shared-backend-services.md).
It ships a Django app plus self-contained submodules that a host project
composes into `INSTALLED_APPS` / `MIDDLEWARE` / settings:

- **Logging** — structured JSON logging + correlation-ID middleware
- **Health** — liveness / readiness endpoints + DB / Redis / Celery checks
- **Cache** — view + method caching decorators, pattern invalidation
- **Rate Limiting** — `rate_limit` decorator + `RateLimitMiddleware`
- **Security** — `SecurityHeadersMiddleware` (CSP + security headers)

plus `monitoring` (Prometheus), `email` (Resend), and `tasks` (Celery base).

Distributed as a PyPI / git library; optional dependencies are grouped as
extras (`[cache]`, `[ratelimit]`, `[monitoring]`, `[email]`, `[logging]`,
`[all]`).

## Setup

```bash
python3 -m pip install -e ".[dev]"   # editable install with dev extras
```

src-layout: the package lives under `src/iil_commons`. `pytest` is configured
with `pythonpath = ["src", "."]` so `import iil_commons` works in a clean
checkout (no editable install needed) and `tests` stays importable for
`DJANGO_SETTINGS_MODULE = "tests.settings"`.

`__version__` is exposed as `iil_commons.__version__` (kept in sync with
`pyproject.toml`).

## Test / lint / types

```bash
make test     # python3 -m pytest
make lint     # python3 -m ruff check .
```

- Tests run against `tests.settings` (no live DB required for the current
  suite). Use `make test`, not raw `pytest`.
- There is **no** `make types` target — mypy is not configured yet (see Known
  issues).

## Architecture (submodule map)

| Module | Responsibility |
|---|---|
| `logging/` | `setup_logging` — structured JSON logging + correlation-ID middleware |
| `health/` | `liveness`, `readiness` views + `DatabaseCheck` / `RedisCheck` / `CeleryCheck` |
| `cache/` | `cached_view`, `cached_method`, `invalidate_pattern` |
| `ratelimit/` | `rate_limit` decorator + `RateLimitMiddleware` |
| `security/` | `SecurityHeadersMiddleware` (CSP + security headers) |
| `monitoring/` | `PrometheusMiddleware` |
| `email/` | `EmailService` (Resend-backed) |
| `tasks/` | `BaseTask` — correlation-ID-aware Celery base task |
| `apps.py` | Django `AppConfig` for the `iil_commons` app |
| `settings.py` | settings helpers (`get_setting`) |

Each submodule declares its own `__all__`; import from the submodule directly.
Submodule imports pull in Django, so the package root deliberately does **not**
re-export them (no eager heavy imports at `import iil_commons`).

## Conventions

- Commits: `[feat|fix|refactor|docs|test|chore](scope): description`.
- Tests: `test_should_<expected_behavior>` (a pytest naming-convention check is
  active; opt out per-test only when justified).
- Keep optional dependencies behind extras; never hard-import an optional
  backend at module import time.

## Release (GATED)

Versioned in `pyproject.toml` + `CHANGELOG.md` (Keep a Changelog). Publishing
(PyPI / tag → release, via `publish.yml`) is a deliberate, **gated** step — not
automatic on merge. Do **not** publish, tag, or release from an agent session
without an explicit human go-ahead. Keep `pyproject.version` and the CHANGELOG
top entry in sync.

## Known issues / gotchas

- `requires-python = ">=3.10"`; CI matrix tests **3.11 + 3.12**. ruff
  `target-version = py310` (the floor). Do not narrow `requires-python`.
- No `mypy` config and no `make types` target — type checking is not gated.
- No coverage gate configured.
- See `AGENT_HANDOVER.md` for current state and next priorities.
