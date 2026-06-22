# AGENT_HANDOVER — iil-django-commons

> Living handover for the next agent/session. Keep this current. For
> architecture and commands see `CLAUDE.md`.

## Current state (2026-06-22)

- Version: **0.3.0** (`pyproject.toml` + `iil_commons.__version__` aligned).
- Tests: green — `make test` → **30 passed, 1 skipped**.
- Lint: `ruff check .` clean (`target-version = py310`).
- CI: `ci.yml` (lint + test on Python **3.11 + 3.12**) + `publish.yml` (gated).
- `requires-python = ">=3.10"`; classifiers list 3.10 / 3.11 / 3.12.

## Recently landed

- **#4** — pytest runs in a clean checkout via src-layout `pythonpath =
  ["src", "."]`, plus a standard `Makefile` (`make test` / `make lint`).
- Agent-readiness: public-API docstring map + `__all__` in
  `src/iil_commons/__init__.py`, `CLAUDE.md`, `AGENT_HANDOVER.md`, and ruff
  `target-version` aligned to the `requires-python` floor (`py310`).

## Known issues / TODO

- No `mypy` config and no `make types` target — type checking is not gated.
- No coverage gate configured.
- Optional backends (Redis, Prometheus, Resend) are behind extras; the current
  test suite does not exercise a live DB / Redis.

## Next priorities

1. Introduce a `[tool.mypy]` config (start lenient) + a `make types` target.
2. Measure suite coverage and add a coverage floor once stable.
3. Expand tests to cover the optional backends (cache/ratelimit/monitoring)
   under their extras.

## Pointers

- Architecture + commands: `CLAUDE.md`.
- Public API surface: docstring map in `src/iil_commons/__init__.py`.
- Changelog: `CHANGELOG.md` (Keep a Changelog).
- Governing ADR: ADR-131 (Shared Backend Services).
