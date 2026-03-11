# iil-django-commons

Shared backend services library for Django projects on the iil.pet platform.

Implements [ADR-131](https://github.com/achimdehnert/platform/blob/main/docs/adr/ADR-131-shared-backend-services.md) — Shared Backend Services for all Django Hub projects.

## Installation

```bash
# Minimal (logging + health only)
pip install git+https://github.com/achimdehnert/iil-django-commons.git@v0.3.0

# With cache support (django-redis)
pip install "iil-django-commons[cache] @ git+https://github.com/achimdehnert/iil-django-commons.git@v0.3.0"

# Full
pip install "iil-django-commons[all] @ git+https://github.com/achimdehnert/iil-django-commons.git@v0.3.0"
```

## Setup

```python
# settings.py
INSTALLED_APPS = [
    "iil_commons",
    ...
]

MIDDLEWARE = [
    "iil_commons.logging.middleware.CorrelationIDMiddleware",
    "iil_commons.logging.middleware.RequestLogMiddleware",
    ...
]

IIL_COMMONS = {
    "LOG_FORMAT": "json",        # "json" | "human"
    "LOG_LEVEL": "INFO",
    "CACHE_DEFAULT_TTL": 300,
    "HEALTH_CHECKS": ["db", "redis"],
}
```

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("", include("iil_commons.health.urls")),
    ...
]
```

## Modules

### Logging
Auto-configured via AppConfig.ready(). Adds `X-Correlation-ID` header and logs `method`, `path`, `status`, `duration_ms`, `user_id` per request.

### Health Checks

| Endpoint | Purpose |
|----------|---------|
| `/livez/` | Liveness — always 200 if process is running |
| `/healthz/` | Readiness — checks DB, Redis, Celery (configurable) |
| `/readyz/` | Alias for `/healthz/` |

### Cache
`@cached_view`, `@cached_method` decorators + `invalidate_pattern()` (requires django-redis).

### Rate Limiting
`@rate_limit(requests, window, key)` decorator + `RateLimitMiddleware` with path-based config.

### Security Headers
`SecurityHeadersMiddleware` — CSP, X-Frame-Options, HSTS, etc.

### Email
Provider-agnostic `EmailService` (SMTP or Resend).

### Tasks
Celery `BaseTask` with auto-retry, exponential backoff, Correlation-ID propagation.

### Monitoring
`PrometheusMiddleware` + `/metrics/` endpoint. No-op if `prometheus_client` not installed.

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

| Phase | Modules | Version |
|-------|---------|---------|
| ✅ Phase 1 | Logging, Health, Cache | v0.1.0 |
| ✅ Phase 2 | Rate Limiting, Security Headers | v0.2.0 |
| ✅ Phase 3 | Email, Celery BaseTask, Prometheus | v0.3.0 |
| Phase 4 | Consumer integration, PyPI publish | v0.4.0 |
