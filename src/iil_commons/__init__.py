"""iil-django-commons — shared backend services for Django Hub projects.

Implements ADR-131 (Shared Backend Services). A Django app (``iil_commons``)
plus a set of self-contained submodules that platform Django projects compose
into ``INSTALLED_APPS`` / ``MIDDLEWARE`` / settings.

Public API is organised by submodule — import from these directly (each
declares its own ``__all__``; the imports pull in Django, so import them
lazily, not at package-import time):

- ``iil_commons.logging``     — ``setup_logging`` (structured JSON logging + correlation IDs)
- ``iil_commons.health``      — ``liveness``/``readiness`` views + DB/Redis/Celery checks
- ``iil_commons.cache``       — ``cached_view``, ``cached_method``, ``invalidate_pattern``
- ``iil_commons.ratelimit``   — ``rate_limit``, ``RateLimitMiddleware``
- ``iil_commons.security``    — ``SecurityHeadersMiddleware`` (CSP + security headers)
- ``iil_commons.monitoring``  — ``PrometheusMiddleware``
- ``iil_commons.email``       — ``EmailService``
- ``iil_commons.tasks``       — ``BaseTask`` (correlation-ID-aware Celery base task)

The Django app config lives in ``iil_commons.apps`` and settings helpers in
``iil_commons.settings``.

``__version__`` is kept in sync with ``pyproject.toml``.
"""

__version__ = "0.3.0"

__all__ = ["__version__"]
